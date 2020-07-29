from typing import Type

from ...core.component import LocalReader, InputConverter
from ...core.specifier import InputFormatSpecifier, DomainSpecifier


class CommonVoiceInputFormatSpecifier(InputFormatSpecifier):
    """
    Specifier of the components for reading Mozilla Common-Voice TSV-format
    speech annotations.
    """
    @classmethod
    def description(cls) -> str:
        return "Reads speech transcriptions in the Mozilla Common-Voice TSV-format"

    @classmethod
    def domain(cls) -> Type[DomainSpecifier]:
        from ...domain.audio.speech import SpeechDomainSpecifier
        return SpeechDomainSpecifier

    @classmethod
    def reader(cls) -> Type[LocalReader]:
        from ..commonvoice.io import CommonVoiceReader
        return CommonVoiceReader

    @classmethod
    def input_converter(cls) -> Type[InputConverter]:
        from ..commonvoice.convert import FromCommonVoice
        return FromCommonVoice
