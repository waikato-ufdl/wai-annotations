import os
import re

from wai.common.cli.options import TypedOption

from ....core.component.util import AnnotationFileProcessor
from ....core.stream import ThenFunction
from ....domain.audio import Audio
from ....domain.audio.speech import SpeechInstance, Transcription
from ..util import LINE_PATTERN


class FestVoxReader(AnnotationFileProcessor[SpeechInstance]):
    """
    Reader of the Festival FestVox speech annotation format.
    """
    # The audio clips may be in a separate folder to the annotations file
    rel_path = TypedOption(
        "--rel-path",
        type=str,
        default=".",
        required=False,
        help="the relative path from the annotations file to the audio files"
    )

    def read_annotation_file(self, filename: str, then: ThenFunction[SpeechInstance]):
        with open(filename, 'r') as file:
            for line in file.readlines():
                match = re.match(LINE_PATTERN, line.strip())

                if match is None:
                    raise ValueError(f"Bad FestVox line: {line}")

                wav_filename, transcription = match.group("filename"), match.group("transcription")

                then(
                    SpeechInstance(
                        Audio.from_file(os.path.join(os.path.dirname(filename), self.rel_path, f"{wav_filename}.wav")),
                        Transcription(transcription)
                    )
                )

    def read_negative_file(self, filename: str, then: ThenFunction[SpeechInstance]):
        yield SpeechInstance(Audio.from_file(filename), None)
