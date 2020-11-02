from typing import Optional, List, Set, Tuple, Type

from wai.common.cli import OptionsList

from ..domain import DomainSpecifier
from ..logging import LoggingEnabled, StreamLogger, get_library_root_logger
from ..plugin import *
from ..specifier import *
from ..specifier.util import instantiate_stage_as_pipeline, specifier_type_string
from ..stream import *
from .error import *
from ._InlineDomainValidator import InlineDomainValidator


class ConversionPipelineBuilder(LoggingEnabled):
    """
    A complete conversion chain. Consists of an input stage, a variable number of intermediate
    stages and an output stage, all optional.
    """
    def __init__(self):
        # The component stages in the conversion chain
        self._source: Optional[Tuple[Pipeline, Type[DomainSpecifier]]] = None
        self._processors: List[Tuple[Pipeline, DomainTransferMap]] = []
        self._sink: Optional[Tuple[Pipeline, Type[DomainSpecifier]]] = None

    @classmethod
    def split_global_options(cls, options: OptionsList) -> Tuple[OptionsList, OptionsList]:
        """
        Splits the global options from the start of an options list.

        :param options:     The full list of options.
        :return:            The global options, and any stage-specific options.
        """
        # Cache the set of available plugins
        available_plugins: Set[str] = get_all_plugin_names()

        # Find where the first stage-specific option starts and split
        for index, option in enumerate(options):
            if option in available_plugins:
                return options[:index], options[index:]

        # If no stage-specific options were provided
        return options, []

    @classmethod
    def split_options(cls, options: OptionsList) -> List[OptionsList]:
        """
        Splits the options list into sub-lists, one for each stage.

        :param options:     The options list.
        :return:            A list of options for each stage.
        """
        # Cache the set of available plugins
        available_plugins: Set[str] = get_all_plugin_names()

        # Add each stage from the options list
        stage_options = []
        for option in options:
            # Skip any initial (global) options
            if len(stage_options) == 0 and option not in available_plugins:
                continue

            # If we've come across a new stage, add a new sub-options list
            if option in available_plugins:
                stage_options.append([])

            stage_options[-1].append(option)

        return stage_options

    @classmethod
    def from_options(cls, options: OptionsList) -> Pipeline:
        """
        Creates a conversion chain from command-line options.

        :param options:     The command-line options.
        :return:            The conversion chain.
        """
        # Split the stage options
        stage_option_lists = cls.split_options(options)

        # Create the empty conversion chain
        conversion_chain = ConversionPipelineBuilder()

        # Add each stage from the options list
        for stage_options in stage_option_lists:
            conversion_chain.add_stage(stage_options[0], stage_options[1:])

        return conversion_chain.to_pipeline()

    def add_stage(self,
                  stage: str,
                  options: OptionsList):
        """
        Adds a stage to the conversion chain.

        :param stage:       The stage to add.
        :param options:     The options to initialise the stage with.
        """
        # Can't add any stages once the sink stage is set
        if self._sink is not None:
            raise StageAfterOutput()

        # Get the specifier for the stage type
        stage_specifier = get_plugin_specifier(stage)

        # Create an instance of the stage as a pipeline
        stage_pipeline = instantiate_stage_as_pipeline(stage_specifier, options)

        # Log that we've created the stage
        self.logger.info(
            f"Created {specifier_type_string(stage_specifier)} stage "
            f"of type '{stage}' "
            f"with options: {options}"
        )

        # Add the stage to the overall pipeline
        if issubclass(stage_specifier, SourceStageSpecifier):
            self._add_source_stage(stage_specifier, stage_pipeline)
        elif issubclass(stage_specifier, ProcessorStageSpecifier):
            self._add_processor_stage(stage_specifier, stage_pipeline)
        elif issubclass(stage_specifier, SinkStageSpecifier):
            self._add_sink_stage(stage_specifier, stage_pipeline)

    def to_pipeline(self) -> Pipeline:
        """
        Exports the built pipeline.
        """
        # Degenerate state: no stages added
        if self._source is None and len(self._processors) == 0 and self._sink is None:
            return Pipeline()

        # Create local state for the actual components of the final pipeline
        source = None
        processors = []
        sink = None

        # Add the source components if any
        if self._source is not None:
            source = self._source[0].source
            processors += self._source[0].processors

        # Add input domain validation and logging
        processors.append(
            InlineDomainValidator(self._source[1])
            if self._source is not None else
            InlineDomainValidator(*self._processors[0][1].keys())
            if len(self._processors) > 0 else
            InlineDomainValidator(self._sink[1])
        )
        processors.append(
            StreamLogger(
                get_library_root_logger().info,
                lambda instance: f"Sourced {instance.data.filename}"
            )
        )

        # Add any processors with domain validation
        for processor_pipeline, domain_transfer_map in self._processors:
            processors += processor_pipeline.processors
            processors.append(InlineDomainValidator(*domain_transfer_map.values()))

        # Add logging to the pipeline to report when an instance is consumed
        processors.append(
            StreamLogger(
                get_library_root_logger().info,
                lambda instance: f"Consuming {instance.data.filename}"
            )
        )

        # Add the sink
        if self._sink is not None:
            processors += self._sink[0].processors
            sink = self._sink[0].sink

        return Pipeline(
            source=source,
            processors=processors,
            sink=sink
        )

    def _add_source_stage(self, stage_specifier: Type[SourceStageSpecifier], stage_pipeline: Pipeline):
        """
        Adds a source stage to the pipeline.

        :param stage_specifier:     The specifier for the source stage.
        :param stage_pipeline:      The instantiated pipeline for the source stage.
        """
        # Can't add another source after the source has been set
        if self._source is not None or len(self._processors) > 0:
            raise InputStageNotFirst()

        # Add the source-stage's components to the overall pipeline
        self._source = stage_pipeline, stage_specifier.domain()

    def _add_processor_stage(self, stage_specifier: Type[ProcessorStageSpecifier], stage_pipeline: Pipeline):
        """
        Adds a processor stage to the pipeline.

        :param stage_specifier:     The specifier for the processor stage.
        :param stage_pipeline:      The instantiated pipeline for the processor stage.
        """
        # Get the set of possible input domains to this processor stage
        possible_input_domains = self._get_possible_input_domains()

        # Get the domain transfer map
        domain_transfer_map = get_domain_transfer_map(stage_specifier, possible_input_domains)

        # If no possible domain transfers exist, error
        if len(domain_transfer_map) == 0:
            raise StageInvalidForDomains(possible_input_domains)

        # Perform a reverse pass to remove now-invalid domains from the processor
        # transfer maps
        self._perform_reverse_domain_pass(set(domain_transfer_map.keys()))

        # Add the stage to the overall pipeline
        self._processors.append((stage_pipeline, domain_transfer_map))

    def _add_sink_stage(self, stage_specifier: Type[SinkStageSpecifier], stage_pipeline: Pipeline):
        """
        Adds a sink stage to the pipeline.

        :param stage_specifier:     The specifier for the sink stage.
        :param stage_pipeline:      The instantiated pipeline for the sink stage.
        """
        # Get the set of possible input domains to this stage
        possible_input_domains = self._get_possible_input_domains()

        # Make sure the sink is suitable for the current domains
        sink_domain = stage_specifier.domain()
        if sink_domain not in possible_input_domains:
            raise StageInvalidForDomains(
                possible_input_domains,
                f"sink-stage is for {sink_domain.name()}"
            )

        # Perform a reverse pass to remove now-invalid domains from the processor
        # transfer maps
        self._perform_reverse_domain_pass({sink_domain})

        # Add the sink-stage to the overall pipeline
        self._sink = stage_pipeline, sink_domain

    def _get_possible_input_domains(self) -> Set[Type[DomainSpecifier]]:
        """
        Gets the set of possible input domains to a new stage based
        on the current set of stages in the pipeline.

        :return:    The set of possible input domains to the new stage.
        """
        return (
            set(self._processors[-1][1].values())
            if len(self._processors) > 0 else
            {self._source[1]}
            if self._source is not None else
            get_all_domains()
        )

    def _perform_reverse_domain_pass(
            self,
            allowed_output_domains: Set[Type[DomainSpecifier]]
    ):
        """
        Performs a reverse-pass over the transfer maps of the processor stages,
        ensuring that each stage only passes domains that can cause the pipeline
        to end in one of the given domains.

        :param allowed_output_domains:  The set of allowed domains at the end of the pipeline.
        """
        # Process each processor stage in reverse order
        for processor_stage in reversed(self._processors):
            # Get the transfer map for the processor stage
            transfer_map = processor_stage[1]

            # Perform the transfer map culling, and stop if it caused no modification
            if not self._reverse_pass_transfer_map(transfer_map, allowed_output_domains):
                return

            # Set the allowed outputs of the previous stage to the allowed inputs
            # to this stage
            allowed_output_domains = set(transfer_map.keys())

    @staticmethod
    def _reverse_pass_transfer_map(
            transfer_map: DomainTransferMap,
            output_domains: Set[Type[DomainSpecifier]]
    ) -> bool:
        """
        Removes entries from the transfer map which don't output a
        domain in the given set.

        :param transfer_map:    The domain transfer map to modify.
        :param output_domains:  The set of valid output domains.
        :return:                Whether the transfer map was modified.
        """
        # Create a set of input domains to remove (the ones which
        # map to unspecified output domains)
        input_domains_for_removal = {
            input_domain
            for input_domain, output_domain in transfer_map.items()
            if output_domain not in output_domains
        }

        # Remove the input domains
        for input_domain in input_domains_for_removal:
            transfer_map.pop(input_domain)

        return len(input_domains_for_removal) > 0
