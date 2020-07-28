from ....core.instance import Instance
from .._AudioInfo import AudioInfo
from ._Transcription import Transcription


class SpeechInstance(Instance[AudioInfo, Transcription]):
    @property
    def is_negative(self) -> bool:
        return len(self.annotations.text) == 0
