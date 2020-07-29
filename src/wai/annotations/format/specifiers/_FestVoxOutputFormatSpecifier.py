from typing import Type

from ...core.component import LocalWriter, OutputConverter
from ...core.specifier import OutputFormatSpecifier, DomainSpecifier


class FestVoxOutputFormatSpecifier(OutputFormatSpecifier):
    """
    Specifier of the components for writing Festival FestVox
    speech annotations.
    """
    @classmethod
    def description(cls) -> str:
        return "Writes speech transcriptions in the Festival FestVox format"

    @classmethod
    def domain(cls) -> Type[DomainSpecifier]:
        from ...domain.audio.speech import SpeechDomainSpecifier
        return SpeechDomainSpecifier

    @classmethod
    def output_converter(cls) -> Type[OutputConverter]:
        from ..festvox.convert import ToFestVox
        return ToFestVox

    @classmethod
    def writer(cls) -> Type[LocalWriter]:
        from ..festvox.io import FestVoxWriter
        return FestVoxWriter
