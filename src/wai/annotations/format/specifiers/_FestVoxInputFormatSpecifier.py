from typing import Type

from ...core.component import LocalReader, InputConverter
from ...core.specifier import InputFormatSpecifier, DomainSpecifier


class FestVoxInputFormatSpecifier(InputFormatSpecifier):
    """
    Specifier of the components for reading Festival FestVox
    speech annotations.
    """
    @classmethod
    def description(cls) -> str:
        return "Reads speech transcriptions in the Festival FestVox format"

    @classmethod
    def domain(cls) -> Type[DomainSpecifier]:
        from ...domain.audio.speech import SpeechDomainSpecifier
        return SpeechDomainSpecifier

    @classmethod
    def reader(cls) -> Type[LocalReader]:
        from ..festvox.io import FestVoxReader
        return FestVoxReader

    @classmethod
    def input_converter(cls) -> Type[InputConverter]:
        from ..festvox.convert import FromFestVox
        return FromFestVox
