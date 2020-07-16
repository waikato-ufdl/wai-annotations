from abc import abstractmethod
from argparse import ArgumentParser, Namespace
from typing import Type

from ..component import CrossDomainConverter
from ._DomainSpecifier import DomainSpecifier
from ._PluginSpecifier import PluginSpecifier


class XDCSpecifier(PluginSpecifier):
    """
    Specifier for a conversion from one domain to another.
    """
    @classmethod
    @abstractmethod
    def from_domain(cls) -> Type[DomainSpecifier]:
        """
        The domain that the conversion takes as input.
        """
        pass

    @classmethod
    @abstractmethod
    def to_domain(cls) -> Type[DomainSpecifier]:
        """
        The domain that the conversion provides as output.
        """
        pass

    @classmethod
    @abstractmethod
    def converter(cls) -> Type[CrossDomainConverter]:
        """
        The type of the actual converter.
        """
        pass

    @classmethod
    def type_string(cls) -> str:
        return "cross-domain converter"

    @classmethod
    def configure_parser(cls, parser: ArgumentParser):
        cls.converter().configure_parser(parser)

    @classmethod
    def stage_instance_from_namespace(cls, namespace: Namespace) -> CrossDomainConverter:
        return cls.converter()(namespace)

    @classmethod
    def format_domain_description(cls) -> str:
        return f"{cls.from_domain().domain_name()} -> {cls.to_domain().domain_name()}"
