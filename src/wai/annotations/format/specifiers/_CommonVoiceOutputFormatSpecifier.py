from typing import Type

from ...core.component import LocalWriter, OutputConverter
from ...core.specifier import OutputFormatSpecifier, DomainSpecifier


class CommonVoiceOutputFormatSpecifier(OutputFormatSpecifier):
    """
    Specifier of the components for writing Mozilla Common-Voice TSV-format
    speech annotations.
    """
    @classmethod
    def description(cls) -> str:
        return "Writes speech transcriptions in the Mozilla Common-Voice TSV-format"

    @classmethod
    def domain(cls) -> Type[DomainSpecifier]:
        from ...domain.audio.speech import SpeechDomainSpecifier
        return SpeechDomainSpecifier

    @classmethod
    def output_converter(cls) -> Type[OutputConverter]:
        from ..commonvoice.convert import ToCommonVoice
        return ToCommonVoice

    @classmethod
    def writer(cls) -> Type[LocalWriter]:
        from ..commonvoice.io import CommonVoiceWriter
        return CommonVoiceWriter
