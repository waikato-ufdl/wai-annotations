from typing import Iterator

from ....core.component import OutputConverter
from ....domain.audio.speech import SpeechInstance
from .._format import FestVoxFormat


class ToFestVox(OutputConverter[SpeechInstance, FestVoxFormat]):
    """
    Converts from the internal speech-domain format to the FestVox format.
    """
    def convert(self, instance: SpeechInstance) -> Iterator[FestVoxFormat]:
        yield FestVoxFormat(instance.file_info, instance.annotations.text)
