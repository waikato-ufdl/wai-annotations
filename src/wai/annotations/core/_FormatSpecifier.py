from typing import Type, Optional

from .components import Reader, ExternalFormatConverter, InternalFormatConverter, Writer


class FormatSpecifier:
    """
    Class which specifies the components available in a given format.
    """
    def __init__(self,
                 reader: Optional[Type[Reader]] = None,
                 input_converter: Optional[Type[ExternalFormatConverter]] = None,
                 output_converter: Optional[Type[InternalFormatConverter]] = None,
                 writer: Optional[Type[Writer]] = None):
        # The specified components
        self._reader: Optional[Type[Reader]] = reader
        self._input_converter: Optional[Type[ExternalFormatConverter]] = input_converter
        self._output_converter: Optional[Type[InternalFormatConverter]] = output_converter
        self._writer: Optional[Type[Writer]] = writer

    @property
    def reader(self) -> Optional[Type[Reader]]:
        """
        Gets the specified reader type.
        """
        return self._reader

    @property
    def input_converter(self) -> Optional[Type[ExternalFormatConverter]]:
        """
        Gets the specified input converter type.
        """
        return self._input_converter

    @property
    def output_converter(self) -> Optional[Type[InternalFormatConverter]]:
        """
        Gets the specified output converter type.
        """
        return self._output_converter

    @property
    def writer(self) -> Optional[Type[Writer]]:
        """
        Gets the specified writer type.
        """
        return self._writer

    @property
    def is_input_ready(self) -> bool:
        """
        Whether this format can be used as the input format of a conversion.
        """
        return self._reader is not None and self._input_converter is not None

    @property
    def is_output_ready(self) -> bool:
        """
        Whether this format can be used as the output format of a conversion.
        """
        return self._output_converter is not None and self._writer is not None

    def __iter__(self):
        yield self._reader
        yield self._input_converter
        yield self._output_converter
        yield self._writer
