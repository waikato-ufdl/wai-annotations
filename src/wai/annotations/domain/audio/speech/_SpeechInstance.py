from typing import Type

from .._AudioInstance import AudioInstance
from ._Transcription import Transcription


class SpeechInstance(AudioInstance[Transcription]):
    """
    An instance in the speech domain.
    """
    @classmethod
    def annotations_type(cls) -> Type[Transcription]:
        return Transcription
