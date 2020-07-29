import os
import re
from typing import Iterator

from wai.common.cli.options import TypedOption

from ....core.component import LocalReader
from ....domain.audio import AudioInfo
from .._format import FestVoxFormat

LINE_PATTERN = '^\\( (?P<filename>.*) "(?P<transcription>.*)" \\)$'


class FestVoxReader(LocalReader[FestVoxFormat]):
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

    def read_annotation_file(self, filename: str) -> Iterator[FestVoxFormat]:
        with open(filename, 'r') as file:
            for line in file.readlines():
                match = re.match(LINE_PATTERN, line.strip())

                if match is None:
                    raise ValueError(f"Bad FestVox line: {line}")

                wav_filename, transcription = match.group("filename"), match.group("transcription")

                yield FestVoxFormat(AudioInfo.from_file(os.path.join(os.path.dirname(filename), self.rel_path, f"{wav_filename}.wav")),
                                    transcription)

    def read_negative_file(self, filename: str) -> Iterator[FestVoxFormat]:
        yield FestVoxFormat(AudioInfo.from_file(filename), "")
