from pkg_resources import EntryPoint
from wai.common.meta.code_repr import (
    CodeRepresentable, CodeRepresentation, code_repr, get_import_dict
)


class RegistryEntry(CodeRepresentable):
    """
    An entry for a plugin format in the registry.
    """
    def __init__(self,
                 name: str,
                 distribution: str,
                 reader: str,
                 input_converter: str,
                 output_converter: str,
                 writer: str):
        self.name: str = name
        self.distribution: str = distribution
        self.reader: str = reader
        self.input_converter: str = input_converter
        self.output_converter: str = output_converter
        self.writer: str = writer

    @classmethod
    def from_entry_point(cls, entry_point: EntryPoint) -> 'RegistryEntry':
        """
        Creates an entry from an entry-point.

        :param entry_point:     The entry-point.
        :return:                The registry entry.
        """
        return RegistryEntry(
            entry_point.module_name + "." + ".".join(entry_point.attrs),
            str(entry_point.dist),
            "", "", "", ""
        )

    @property
    def is_available_for_input(self) -> bool:
        """
        Whether this format can be used for input.
        """
        return self.reader != "" and self.input_converter != ""

    @property
    def is_available_for_output(self) -> bool:
        """
        Whether this format can be used for output.
        """
        return self.output_converter != "" and self.writer != ""

    def set_components(self, reader: str, input_converter: str, output_converter: str, writer: str):
        """
        Sets the components for this entry.
        """
        self.reader = reader
        self.input_converter = input_converter
        self.output_converter = output_converter
        self.writer = writer

    def __eq__(self, other):
        return (
                isinstance(other, RegistryEntry)
                and other.name == self.name
                and other.distribution == self.distribution
        )

    def code_repr(self) -> CodeRepresentation:
        return (
            get_import_dict(code_repr(RegistryEntry)),
            f"RegistryEntry("
            f"'{self.name}', "
            f"'{self.distribution}', "
            f"'{self.reader}', "
            f"'{self.input_converter}', "
            f"'{self.output_converter}', "
            f"'{self.writer}')"
        )
