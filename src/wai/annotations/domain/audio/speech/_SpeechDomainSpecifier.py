from typing import Type

from ....core.specifier import DomainSpecifier
from .._AudioInfo import AudioInfo
from ._SpeechInstance import SpeechInstance
from ._Transcription import Transcription


class SpeechDomainSpecifier(DomainSpecifier):
    """
    Domain specifier for audio recordings of speech annotated the
    transcription of the spoken words.
    """
    @classmethod
    def domain_name(cls) -> str:
        return "Speech Domain"

    @classmethod
    def file_type(cls) -> Type[AudioInfo]:
        return AudioInfo

    @classmethod
    def annotations_type(cls) -> Type[Transcription]:
        return Transcription

    @classmethod
    def instance_class(cls) -> Type[SpeechInstance]:
        return SpeechInstance