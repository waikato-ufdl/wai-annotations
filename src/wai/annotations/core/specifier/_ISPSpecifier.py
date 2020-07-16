from abc import abstractmethod
from argparse import ArgumentParser, Namespace
from typing import Type, Set, Optional

from ..component import InlineStreamProcessor
from ._DomainSpecifier import DomainSpecifier
from ._PluginSpecifier import PluginSpecifier


class ISPSpecifier(PluginSpecifier):
    """
    Specifies an inline stream-processor.
    """
    @classmethod
    @abstractmethod
    def domains(cls) -> Optional[Set[Type[DomainSpecifier]]]:
        """
        Gets the domains that this ISP can operate on. If it
        can work for any domain, it should return None.
        """
        pass

    @classmethod
    @abstractmethod
    def processor_type(cls) -> Type[InlineStreamProcessor]:
        """
        Gets the type of the ISP.
        """
        pass

    @classmethod
    def type_string(cls) -> str:
        return "inline stream-processor"

    @classmethod
    def configure_parser(cls, parser: ArgumentParser):
        cls.processor_type().configure_parser(parser)

    @classmethod
    def stage_instance_from_namespace(cls, namespace: Namespace) -> InlineStreamProcessor:
        return cls.processor_type()(namespace)

    @classmethod
    def format_domain_description(cls) -> str:
        # Get the set of domains that this ISP works with
        domains = cls.domains()

        # If the set is None, works with any domain
        if domains is None:
            return "Any"

        # If the set is empty, works with no domains. Not really a useful
        # case, but technically possible
        if len(domains) == 0:
            return "None"

        return ", ".join((domain.domain_name() for domain in domains))
