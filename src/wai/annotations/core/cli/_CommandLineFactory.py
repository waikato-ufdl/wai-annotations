from abc import abstractmethod
from argparse import ArgumentParser, Namespace
from typing import Generic, TypeVar, Type, Dict, Any

# Type variable for the related class that this factory produces
RelatedClass = TypeVar("RelatedClass")


class CommandLineFactory(Generic[RelatedClass]):
    """
    Base class for factories which produce instances of a related
    class by parsing command-line arguments.
    """
    @classmethod
    @abstractmethod
    def related_class(cls) -> Type[RelatedClass]:
        """
        Gets the class that this factory instantiates.
        """
        pass

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
    def instance_from_namespace(cls, namespace: Namespace) -> RelatedClass:
        """
        Creates an instance of this class from the provided namespace.

        :param namespace:   The namespace containing the parsed arguments.
        :return:            The instance.
        """
        return cls.related_class()(**cls.determine_kwargs_from_namespace(namespace))
