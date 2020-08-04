from typing import Optional, Type, List, Union, Set, Iterator, Tuple, Iterable, IO

from wai.common.cli import OptionsList

from ..component import *
from ..error import *
from ..instance import Instance
from ..logging import LoggingEnabled
from ..plugin import get_plugin_specifier_of_known_type, get_all_plugin_names
from ..specifier import *
from ..stage import InputStage, OutputStage
from ._InlineDomainValidator import InlineDomainValidator


class ConversionChain(LoggingEnabled):
    """
    A complete conversion chain. Consists of an input stage, a variable number of intermediate
    stages and an output stage, all optional.
    """
    def __init__(self):
        # The component stages in the conversion chain
        self._input_stage: Optional[InputStage] = None
        self._intermediate_stages: List[Union[InlineStreamProcessor, CrossDomainConverter]] = []
        self._output_stage: Optional[OutputStage] = None

        # Domain tracking for ensuring compatibility between components and instances. Each set
        # is the group of allowed domains at the input/output of the intermediate stage pipeline,
        # or None if any domain is allowed.
        self._input_domains: Optional[Set[Type[DomainSpecifier]]] = None
        self._output_domains: Optional[Set[Type[DomainSpecifier]]] = None

    @property
    def has_input(self) -> bool:
        """
        Whether this conversion chain has an input stage.
        """
        return self._input_stage is not None

    @property
    def has_output(self) -> bool:
        """
        Whether this conversion chain has an output stage.
        """
        return self._output_stage is not None

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
    def from_options(cls, options: OptionsList) -> 'ConversionChain':
        """
        Creates a conversion chain from command-line options.

        :param options:     The command-line options.
        :return:            The conversion chain.
        """
        # Split the stage options
        stage_option_lists = cls.split_options(options)

        # Create the empty conversion chain
        conversion_chain = ConversionChain()

        # Add each stage from the options list
        for stage_options in stage_option_lists:
            conversion_chain.add_stage(stage_options[0], stage_options[1:])

        return conversion_chain

    def add_stage(self,
                  stage: str,
                  options: OptionsList):
        """
        Adds a stage to the conversion chain.

        :param stage:       The stage to add.
        :param options:     The options to initialise the stage with.
        """
        # Get the specifier for the stage type
        stage_specifier = get_plugin_specifier_of_known_type(stage)

        # Add logging to the instantiation of stages
        def instantiate_stage_and_log():
            stage_instance = stage_specifier.instantiate_stage(options)
            self.logger.info(F"Created {stage_specifier.type_string()} stage of type '{stage}' with options: {options}")
            return stage_instance

        # First stage
        if self._input_stage is None and len(self._intermediate_stages) == 0 and self._output_stage is None:
            if issubclass(stage_specifier, InputFormatSpecifier):
                self._input_stage = instantiate_stage_and_log()
                self._input_domains = self._output_domains = {stage_specifier.domain()}
            elif issubclass(stage_specifier, OutputFormatSpecifier):
                self._output_stage = instantiate_stage_and_log()
                self._input_domains = self._output_domains = {stage_specifier.domain()}
            else:
                self._intermediate_stages.append(instantiate_stage_and_log())
                if issubclass(stage_specifier, ISPSpecifier):
                    self._input_domains = self._output_domains = stage_specifier.domains()
                else:
                    self._input_domains = {stage_specifier.from_domain()}
                    self._output_domains = {stage_specifier.to_domain()}

        # Subsequent stages
        else:
            # Can't add stages after the output
            if self._output_stage is not None:
                raise StageAfterOutput()

            # Can only set the input as the first stage
            if issubclass(stage_specifier, InputFormatSpecifier):
                raise InputStageNotFirst()

            # If it's an output format
            if issubclass(stage_specifier, OutputFormatSpecifier):
                # Make sure the format is for the current output domain
                if self._output_domains is not None and stage_specifier.domain() not in self._output_domains:
                    raise BadDomain(f"Attempted to add output stage for domain "
                                    f"{stage_specifier.domain().domain_name()} ({stage}) "
                                    f"when previous stages limit "
                                    f"domains to: {', '.join(domain.domain_name() for domain in self._output_domains)}")

                # If the current input domain has more than one option, then all
                # intermediaries must be ISPs, so the input domain becomes the domain
                # of this format
                if self._input_domains is None or len(self._input_domains) > 1:
                    self._input_domains = {stage_specifier.domain()}

                self._output_stage = instantiate_stage_and_log()
                return

            # Make sure the ISP/XDC works with the current domain
            if issubclass(stage_specifier, ISPSpecifier):
                # Make sure the ISP can work with the current set of output domains, and calculate the
                # new set of output domains
                if self._output_domains is not None and stage_specifier.domains() is not None:
                    # Get the set of domains that the stage can work with out of the
                    # current set of possible output domains
                    common_domains = self._output_domains.intersection(stage_specifier.domains())

                    # If there are none to work with, error
                    if len(self._output_domains) == 0:
                        raise BadDomain(f"No common domains between current output set "
                                        f"({', '.join(domain.domain_name() for domain in self._output_domains)}) and "
                                        f"those operable by ISP {stage} "
                                        f"({', '.join(domain.domain_name() for domain in stage_specifier.domains())})")

                    self._output_domains = common_domains

                elif self._output_domains is None:
                    self._output_domains = stage_specifier.domains()

                # Add the stage to the intermediaries
                self._intermediate_stages.append(instantiate_stage_and_log())

                # If the current input domain has more than one option, then all
                # intermediaries must be ISPs, so the input domains become the same
                # as the output domains
                if self._input_domains is None or len(self._input_domains) > 1:
                    self._input_domains = self._output_domains

            # issubclass(stage, XDCSpecifier) == True
            else:
                # Make sure the current output domain matches the input domain for the XDC
                if self._output_domains is not None and stage_specifier.from_domain() not in self._output_domains:
                    raise BadDomain(f"XDC {stage} ({stage_specifier.from_domain().domain_name()}) "
                                    f"is not applicable to current set of possible domains: "
                                    f"{', '.join(domain.domain_name() for domain in self._output_domains)}")

                # Add the stage to the intermediaries
                self._intermediate_stages.append(instantiate_stage_and_log())

                # If the current input domain has more than one option, then all
                # intermediaries must be ISPs, so the input domain must be input domain
                # of the XDC
                if self._input_domains is None or len(self._input_domains) > 1:
                    self._input_domains = {stage_specifier.from_domain()}

                self._output_domains = {stage_specifier.to_domain()}

    def load(self) -> Iterator[Instance]:
        """
        If this conversion chain has an input reader, uses it to
        produce a converted stream of instances in the output domain.

        :return:                                An iterator over the converted instances.
        :raises ConversionChainHasNoReader:     If the chain isn't configured with an input stage.
        """
        # Make sure we have an input
        if self._input_stage is None:
            raise ConversionChainHasNoReader()

        return self.process(self._input_stage.load())

    def save(self, instances: Optional[Iterable[Instance]] = None):
        """
        Saves the given instances to disk using the configured output
        writer.

        :param instances:                       The instances to write, or None to load instances
                                                from the input stage.
        :raises ConversionChainHasNoWriter:     If the chain isn't configured with an output stage.
        :raises ConversionChainHasNoReader:     If the chain isn't configured with an input stage and
                                                the instances aren't provided explicitly.
        """
        # Make sure we have an output
        if self._output_stage is None:
            raise ConversionChainHasNoWriter()

        # Load the instances if not given explicitly, or process
        # the given instances
        if instances is not None:
            instances = self.process(instances)
        else:
            instances = self.load()

        # Write the instances
        self._output_stage.save(instances)

    def file_iterator(self, instances: Optional[Iterable[Instance]] = None) -> Iterator[Tuple[str, IO[bytes]]]:
        """
        Converts the given instances to the actual files they are written to.

        :param instances:                       The instances to write, or None to load instances
                                                from the input stage.
        :return:                                An iterator of filename, file-contents pairs.
        :raises ConversionChainHasNoWriter:     If the chain isn't configured with an output stage.
        :raises ConversionChainHasNoReader:     If the chain isn't configured with an input stage and
                                                the instances aren't provided explicitly.
        """
        # Make sure we have an output
        if self._output_stage is None:
            raise ConversionChainHasNoWriter()

        # Load the instances if not given explicitly, or process
        # the given instances
        if instances is not None:
            instances = self.process(instances)
        else:
            instances = self.load()

        # Return the files
        return self._output_stage.file_iterator(instances)

    def process(self, input: Iterable[Instance]) -> Iterator[Instance]:
        """
        Processes the input using the intermediary stages.

        :param input:   The input in one of the input domains.
        :return:        An iterator over the converted instances.
        """
        # Attach a domain validator to the input stream if the input
        # domain is restricted
        if self._input_domains is not None:
            input = InlineDomainValidator(*self._input_domains).process(input)

        for stage in self._intermediate_stages:
            if isinstance(stage, InlineStreamProcessor):
                input = stage.process(input)
            else:
                input = stage.convert(input)

        yield from input
