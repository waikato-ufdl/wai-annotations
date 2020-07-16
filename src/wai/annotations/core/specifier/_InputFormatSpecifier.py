from abc import abstractmethod
from argparse import ArgumentParser, Namespace
from typing import Type

from ..component import Reader, InputConverter
from ..stage import InputStage
from ._DomainSpecifier import DomainSpecifier
from ._PluginSpecifier import PluginSpecifier


class InputFormatSpecifier(PluginSpecifier):
    """
    Class which specifies the components available to read a given format.
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
    def reader(cls) -> Type[Reader]:
        """
        Gets the specified reader type.
        """
        pass

    @classmethod
    @abstractmethod
    def input_converter(cls) -> Type[InputConverter]:
        """
        Gets the specified input converter type.
        """
        pass

    @classmethod
    def type_string(cls) -> str:
        return "input format"

    @classmethod
    def configure_parser(cls, parser: ArgumentParser):
        cls.reader().configure_parser(parser)
        cls.input_converter().configure_parser(parser)

    @classmethod
    def stage_instance_from_namespace(cls, namespace: Namespace) -> InputStage:
        return InputStage(
            cls.reader()(namespace),
            cls.input_converter()(namespace)
        )

    @classmethod
    def format_domain_description(cls) -> str:
        return cls.domain().domain_name()
