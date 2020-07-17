from typing import Iterator

from ....core.component import OutputConverter
from ....domain.audio.speech import SpeechInstance
from .._format import CommonVoiceFormat


class ToCommonVoice(OutputConverter[SpeechInstance, CommonVoiceFormat]):
    """
    Converts from the internal speech-domain format to the CommonVoice format.
    """
    def convert(self, instance: SpeechInstance) -> Iterator[CommonVoiceFormat]:
        yield CommonVoiceFormat(instance.file_info,
                                "",
                                instance.annotations.text,
                                0, 0, None, None, None, "", "")
