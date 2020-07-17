from typing import Iterator

from ....core.component import InputConverter
from ....domain.audio.speech import Transcription, SpeechInstance
from .._format import FestVoxFormat


class FromFestVox(InputConverter[FestVoxFormat, SpeechInstance]):
    """
    Converts from the Festival FestVox format to the internal speech-domain format.
    """
    def convert(self, instance: FestVoxFormat) -> Iterator[SpeechInstance]:
        transcription = Transcription(instance.transcription)
        yield SpeechInstance(instance.file, transcription)
