from typing import Type, Tuple

from ....core.component import Component
from ....core.domain import DomainSpecifier
from ....core.specifier import SourceStageSpecifier


class CommonVoiceInputFormatSpecifier(SourceStageSpecifier):
    """
    Specifier of the components for reading Mozilla Common-Voice TSV-format
    speech annotations.
    """
    @classmethod
    def description(cls) -> str:
        return "Reads speech transcriptions in the Mozilla Common-Voice TSV-format"

    @classmethod
    def components(cls) -> Tuple[Type[Component], ...]:
        from ....core.component.util import LocalFilenameSource
        from ..component import CommonVoiceReader
        return LocalFilenameSource, CommonVoiceReader

    @classmethod
    def domain(cls) -> Type[DomainSpecifier]:
        from ....domain.audio.speech import SpeechDomainSpecifier
        return SpeechDomainSpecifier
