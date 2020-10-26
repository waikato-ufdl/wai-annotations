from typing import Type, Tuple

from ....core.component import Component
from ....core.domain import DomainSpecifier
from ....core.specifier import SourceStageSpecifier


class FestVoxInputFormatSpecifier(SourceStageSpecifier):
    """
    Specifier of the components for reading Festival FestVox
    speech annotations.
    """
    @classmethod
    def description(cls) -> str:
        return "Reads speech transcriptions in the Festival FestVox format"

    @classmethod
    def components(cls) -> Tuple[Type[Component], ...]:
        from ....core.component.util import LocalFilenameSource
        from ..component import FestVoxReader
        return LocalFilenameSource, FestVoxReader

    @classmethod
    def domain(cls) -> Type[DomainSpecifier]:
        from ....domain.audio.speech import SpeechDomainSpecifier
        return SpeechDomainSpecifier
