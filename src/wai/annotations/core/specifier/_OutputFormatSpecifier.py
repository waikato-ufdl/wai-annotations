from abc import abstractmethod
from argparse import ArgumentParser, Namespace
from typing import Type

from ..component import OutputConverter, Writer
from ..stage import OutputStage
from ._DomainSpecifier import DomainSpecifier
from ._PluginSpecifier import PluginSpecifier


class OutputFormatSpecifier(PluginSpecifier):
    """
    Class which specifies the components available to write a given format.
    """
    @classmethod
    @abstractmethod
    def domain(cls) -> Type[DomainSpecifier]:
        """
        The domain of the format.
        """
        pass

    @classmethod
    @abstractmethod
    def output_converter(cls) -> Type[OutputConverter]:
        """
        Gets the specified output converter type.
        """
        pass

    @classmethod
    @abstractmethod
    def writer(cls) -> Type[Writer]:
        """
        Gets the specified writer type.
        """
        pass

    @classmethod
    def type_string(cls) -> str:
        return "output format"

    @classmethod
    def configure_parser(cls, parser: ArgumentParser):
        cls.writer().configure_parser(parser)
        cls.output_converter().configure_parser(parser)

    @classmethod
    def stage_instance_from_namespace(cls, namespace: Namespace) -> OutputStage:
        return OutputStage(
            cls.writer()(namespace),
            cls.output_converter()(namespace)
        )

    @classmethod
    def format_domain_description(cls) -> str:
        return cls.domain().domain_name()
