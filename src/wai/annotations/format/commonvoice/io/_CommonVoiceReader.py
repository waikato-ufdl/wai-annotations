import csv
import os
from typing import Iterator

from wai.common.cli.options import TypedOption

from ....core.component import LocalReader
from ....domain.audio import AudioInfo
from ..util import CommonVoiceDialect, EXPECTED_HEADER
from .._format import CommonVoiceFormat


class CommonVoiceReader(LocalReader[CommonVoiceFormat]):
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

    def read_annotation_file(self, filename: str) -> Iterator[CommonVoiceFormat]:
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
                yield CommonVoiceFormat(AudioInfo.from_file(os.path.join(os.path.dirname(filename), self.rel_path, row["path"])),
                                        **{key: value for key, value in row.items() if key != "path"})

    def read_negative_file(self, filename: str) -> Iterator[CommonVoiceFormat]:
        yield CommonVoiceFormat(AudioInfo.from_file(filename),
                                "", "", 0, 0, None, None, None, "", "")
