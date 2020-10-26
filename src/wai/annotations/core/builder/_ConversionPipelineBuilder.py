from typing import Optional, List, Set, Tuple, Type

from wai.common.cli import OptionsList

from ..domain import DomainSpecifier
from ..logging import LoggingEnabled, StreamLogger
from ..plugin import get_plugin_specifier, get_all_plugin_names
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
        self._source: Optional[StreamSource] = None
        self._processors: List[StreamProcessor] = []
        self._sink: Optional[StreamSink] = None

        # The current domain of the pipeline for "static" type-checking
        self._current_domain: Optional[Type[DomainSpecifier]] = None

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
        return Pipeline(
            source=self._source,
            processors=self._processors,
            sink=self._sink
        )

    def _add_source_stage(self, stage_specifier: Type[SourceStageSpecifier], stage_pipeline: Pipeline):
        """
        Adds a source stage to the pipeline.

        :param stage_specifier:     The specifier for the source stage.
        :param stage_pipeline:      The instantiated pipeline for the source stage.
        """
        # Can't add another source after the source has been set
        if self._source is not None:
            raise InputStageNotFirst()

        # Add the source-stage's components to the overall pipeline
        self._source = stage_pipeline.source
        self._processors += stage_pipeline.processors

        # Track the domain of the pipeline
        self._current_domain = stage_specifier.domain()

        # Add a validator to ensure the domain is that reported by the specifier
        self._processors.append(InlineDomainValidator(self._current_domain))

        # Add logging to the pipeline to report when an instance is loaded
        self._processors.append(
            StreamLogger(
                self.logger.info,
                lambda instance: f"Sourced {instance.data.filename}"
            )
        )

    def _add_processor_stage(self, stage_specifier: Type[ProcessorStageSpecifier], stage_pipeline: Pipeline):
        """
        Adds a processor stage to the pipeline.

        :param stage_specifier:     The specifier for the processor stage.
        :param stage_pipeline:      The instantiated pipeline for the processor stage.
        """
        # Can't add processors until a source has been added
        if self._source is None:
            raise InputStageNotFirst()

        # Update the pipeline's domain
        try:
            self._current_domain = stage_specifier.domain_transfer_function(self._current_domain)
        except Exception as e:
            raise StageInvalidForDomain(self._current_domain, str(e)) from e

        # Add the processor-stage's components to the overall pipeline
        self._processors += stage_pipeline.processors

        # Add domain validation for the processor
        self._processors.append(InlineDomainValidator(self._current_domain))

    def _add_sink_stage(self, stage_specifier: Type[SinkStageSpecifier], stage_pipeline: Pipeline):
        """
        Adds a sink stage to the pipeline.

        :param stage_specifier:     The specifier for the sink stage.
        :param stage_pipeline:      The instantiated pipeline for the sink stage.
        """
        # Can't add a sink until a source has been added
        if self._source is None:
            raise InputStageNotFirst()

        # Make sure the sink is suitable for the current domain
        if self._current_domain is not stage_specifier.domain():
            raise StageInvalidForDomain(self._current_domain, f"sink is for {stage_specifier.domain().name()}")

        # Add logging to the pipeline to report when an instance is consumed
        self._processors.append(
            StreamLogger(
                self.logger.info,
                lambda instance: f"Consuming {instance.data.filename}"
            )
        )

        # Add the sink-stage's components to the overall pipeline
        self._processors += stage_pipeline.processors
        self._sink = stage_pipeline.sink
