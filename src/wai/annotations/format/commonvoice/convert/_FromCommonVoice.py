from typing import Iterator

from ....core.component import InputConverter
from ....domain.audio.speech import Transcription, SpeechInstance
from .._format import CommonVoiceFormat


class FromCommonVoice(InputConverter[CommonVoiceFormat, SpeechInstance]):
    """
    Converts from the Common-Voice format to the internal speech-domain format.
    """
    def convert(self, instance: CommonVoiceFormat) -> Iterator[SpeechInstance]:
        transcription = Transcription(instance.sentence)
        yield SpeechInstance(instance.file, transcription)
