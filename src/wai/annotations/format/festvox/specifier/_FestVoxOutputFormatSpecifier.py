from typing import Type, Tuple

from ....core.component import Component
from ....core.domain import DomainSpecifier
from ....core.specifier import SinkStageSpecifier


class FestVoxOutputFormatSpecifier(SinkStageSpecifier):
    """
    Specifier of the components for writing Festival FestVox
    speech annotations.
    """
    @classmethod
    def description(cls) -> str:
        return "Writes speech transcriptions in the Festival FestVox format"

    @classmethod
    def components(cls) -> Tuple[Type[Component], ...]:
        from ..component import FestVoxWriter
        return FestVoxWriter,

    @classmethod
    def domain(cls) -> Type[DomainSpecifier]:
        from ....domain.audio.speech import SpeechDomainSpecifier
        return SpeechDomainSpecifier
