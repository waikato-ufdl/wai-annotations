from typing import Type

from ....core.domain import DomainSpecifier
from .._Audio import Audio
from ._SpeechInstance import SpeechInstance
from ._Transcription import Transcription

DESCRIPTION = """Transcriptions of recorded speech.

The speech domain covers audio data of people speaking natural languages, annotated with text transcribing the verbal
contents of the audio. Instances in this domain are an audio file and a string containing the transcription.
"""


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
        return DESCRIPTION
    
    @classmethod
    def data_type(cls) -> Type[Audio]:
        return Audio
    
    @classmethod
    def annotations_type(cls) -> Type[Transcription]:
        return Transcription

    @classmethod
    def instance_type(cls) -> Type[SpeechInstance]:
        return SpeechInstance
