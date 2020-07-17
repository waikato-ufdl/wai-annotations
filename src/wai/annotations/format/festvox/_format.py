from ...domain.audio import AudioInfo


class FestVoxFormat:
    """
    Representation of the external FestVox speech annotation format.
    """
    def __init__(self, file: AudioInfo, transcription: str):
        self._file: AudioInfo = file
        self._transcription: str = transcription

    @property
    def file(self) -> AudioInfo:
        return self._file

    @property
    def transcription(self) -> str:
        return self._transcription
