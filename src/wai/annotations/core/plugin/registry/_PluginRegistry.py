from typing import Dict, Iterable, Set, Optional, Type

from pkg_resources import EntryPoint

from wai.common.cli import CLIFactory
from wai.common.meta.code_repr import (
    CodeRepresentable, CodeRepresentation, code_repr, get_import_dict, combine_import_dicts,
    get_code
)

from ..error import MultiplyDefinedFormats
from ._RegistryEntry import RegistryEntry


class PluginRegistry(CodeRepresentable):
    """
    Class which represents the plugins registered with the system.
    """
    def __init__(self, **entries: RegistryEntry):
        self._entries: Dict[str, RegistryEntry] = entries

    @classmethod
    def from_entry_points(cls,
                          entry_points: Iterable[EntryPoint]) -> 'PluginRegistry':
        """
        Creates the registry from entry-points.

        :param entry_points:    The entry-points to process.
        :return:                A plugin registry object.
        """
        # Consume the iterable
        entry_points = tuple(entry_points)

        # Make sure no formats are multiply-defined
        MultiplyDefinedFormats.check_entry_points(entry_points)

        return PluginRegistry(**{entry_point.name: RegistryEntry.from_entry_point(entry_point)
                                 for entry_point in entry_points})

    def get_formats(self) -> Set[str]:
        """
        Gets the set of known format identifiers.
        """
        return set(self._entries.keys())

    def get_available_input_formats(self) -> Set[str]:
        """
        Gets the set of formats available for input.
        """
        return {format
                for format, entry in self._entries.items()
                if entry.is_available_for_input}

    def get_available_output_formats(self) -> Set[str]:
        """
        Gets the set of formats available for output.
        """
        return {format
                for format, entry in self._entries.items()
                if entry.is_available_for_output}

    def ensure_format(self, format: str, input: Optional[bool] = None):
        """
        Raises an error if the format is not known.

        :param format:  The format to check.
        :param input:   True to check the format can be read,
                        False to check the format can be written,
                        None (the default) to check both.
        """
        # Check the given format exists at all
        if format not in self._entries:
            raise ValueError(f"Unknown format '{format}'. Available formats are {self._entries.keys()}")

        entry = self._entries[format]

        check = (entry.is_available_for_input and entry.is_available_for_output if input is None else
                 entry.is_available_for_input if input else
                 entry.is_available_for_output)
        check_string = ("readable/writable" if input is None else
                        "readable" if input else
                        "writable")
        if not check:
            raise ValueError(f"Format '{format}' is not currently implemented as a {check_string} format")

    @staticmethod
    def get_factory_by_name(factory_name: str) -> Type[CLIFactory]:
        """
        Gets a factory class by name.

        :param factory_name:    The name of the factory class.
        :return:                The factory class.
        """
        from importlib import import_module
        factory_module = import_module(f"..factories._{factory_name}", __package__)
        return getattr(factory_module, factory_name)

    def get_reader_factory(self, format: str) -> Optional[Type[CLIFactory]]:
        """
        Gets the reader factory for a given format.

        :param format:  The format identifier.
        :return:        The reader factory for the format.
        """
        # Check the format is known
        self.ensure_format(format, True)

        # Get the reader factory for the format
        return self.get_factory_by_name(self._entries[format].reader)

    def get_external_format_converter_factory(self, format: str) -> Optional[Type[CLIFactory]]:
        """
        Gets the external format converter factory for a given format.

        :param format:  The format identifier.
        :return:        The external format converter factory for the format.
        """
        # Check the format is known
        self.ensure_format(format, True)

        # Get the external format converter factory for the format
        return self.get_factory_by_name(self._entries[format].input_converter)

    def get_internal_format_converter_factory(self, format: str) -> Optional[Type[CLIFactory]]:
        """
        Gets the internal format converter factory for a given format.

        :param format:  The format identifier.
        :return:        The internal format converter factory for the format.
        """
        # Check the format is known
        self.ensure_format(format, False)

        # Get the internal format converter factory for the format
        return self.get_factory_by_name(self._entries[format].output_converter)

    def get_writer_factory(self, format: str) -> Optional[Type[CLIFactory]]:
        """
        Gets the writer factory for a given format.

        :param format:  The format identifier.
        :return:        The writer factory for the format.
        """
        # Check the format is known
        self.ensure_format(format, False)

        # Get the reader factory for the format
        return self.get_factory_by_name(self._entries[format].writer)

    def __eq__(self, other):
        if not isinstance(other, PluginRegistry):
            return False

        if not set(other._entries.keys()) == set(self._entries.keys()):
            return False

        for format in self._entries:
            if self._entries[format] != other._entries[format]:
                return False

        return True

    def __getitem__(self, item):
        return self._entries[item]

    def code_repr(self) -> CodeRepresentation:
        return (
            combine_import_dicts(
                get_import_dict(code_repr(PluginRegistry)),
                get_import_dict(code_repr(RegistryEntry))
            ),
            "PluginRegistry(" +
            ", ".join(f"{key}={get_code(code_repr(value))}"
                      for key, value in self._entries.items()) +
            ")"
        )
