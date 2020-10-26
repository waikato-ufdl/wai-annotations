import csv
import os

from wai.common.cli.options import TypedOption

from ....core.component.util import AnnotationFileProcessor
from ....core.stream import ThenFunction
from ....domain.audio import Audio
from ....domain.audio.speech import SpeechInstance, Transcription
from ..util import CommonVoiceDialect, EXPECTED_HEADER


class CommonVoiceReader(AnnotationFileProcessor[SpeechInstance]):
    """
    Reader of Mozilla's CommonVoice speech annotation format.
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
        with open(filename, 'r', newline='') as file:
            # Consume the header
            header = file.readline()

            # Make sure the header is what we expect
            if header != EXPECTED_HEADER + '\n':
                raise ValueError(f"Expected header: {EXPECTED_HEADER}\n"
                                 f"Seen header: {header}")

            # Yield rows from the file
            for row in csv.DictReader(file,
                                      EXPECTED_HEADER.split('\t'),
                                      dialect=CommonVoiceDialect):
                then(
                    SpeechInstance(
                        Audio.from_file(os.path.join(os.path.dirname(filename), self.rel_path, row["path"])),
                        Transcription(row['sentence'])
                    )
                )

    def read_negative_file(self, filename: str, then: ThenFunction[SpeechInstance]):
        then(SpeechInstance(Audio.from_file(filename), None))
