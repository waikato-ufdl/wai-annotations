from ....core.instance import Instance
from .._AudioInfo import AudioInfo
from ._Transcription import Transcription


class SpeechInstance(Instance[AudioInfo, Transcription]):
    pass
