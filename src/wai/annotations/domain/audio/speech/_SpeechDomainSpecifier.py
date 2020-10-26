from typing import Type

from ....core.domain import DomainSpecifier
from .._Audio import Audio
from ._SpeechInstance import SpeechInstance
from ._Transcription import Transcription


class SpeechDomainSpecifier(DomainSpecifier[Audio, Transcription]):
    """
    Domain specifier for audio recordings of speech annotated the
    transcription of the spoken words.
    """
    @classmethod
    def name(cls) -> str:
        return "Speech Domain"
    
    @classmethod
    def description(cls) -> str:
        return "Transcriptions of recorded speech"
    
    @classmethod
    def data_type(cls) -> Type[Audio]:
        return Audio
    
    @classmethod
    def annotations_type(cls) -> Type[Transcription]:
        return Transcription

    @classmethod
    def instance_type(cls) -> Type[SpeechInstance]:
        return SpeechInstance
