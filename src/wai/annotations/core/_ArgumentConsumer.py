from abc import ABC, abstractmethod
from argparse import ArgumentParser, Namespace
from typing import Any, Dict


class ArgumentConsumer(ABC):
    """
    Interface for classes that can be instantiated by parsing
    command-line arguments.
    """
    @classmethod
    @abstractmethod
    def configure_parser(cls, parser: ArgumentParser):
        """
        Configures the arguments this class expects for instantiation.

        :param parser:  An argument parser to configure.
        """
        pass

    @classmethod
    @abstractmethod
    def determine_kwargs_from_namespace(cls, namespace: Namespace) -> Dict[str, Any]:
        """
        Formats the arguments in the provided namespace into a kwarg
        dictionary expected by __init__ for this class.

        :param namespace:   The namespace containing the parsed arguments.
        :return:            The kwargs.
        """
        pass

    @classmethod
    def instance_from_namespace(cls, namespace: Namespace):
        """
        Creates an instance of this class from the provided namespace.

        :param namespace:   The namespace containing the parsed arguments.
        :return:            The instance.
        """
        return cls(**cls.determine_kwargs_from_namespace(namespace))
