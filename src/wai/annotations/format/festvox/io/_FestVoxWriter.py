import os
from typing import Iterable

from ....core.component import SeparateFileWriter
from ....domain.audio import AudioInfo
from .._format import FestVoxFormat


class FestVoxWriter(SeparateFileWriter[FestVoxFormat]):
    """
    Writer of the Festival FestVox speech annotation format.
    """
    def write_annotations_only(self, instances: Iterable[FestVoxFormat], path: str):
        with open(path, 'w') as file:
            for instance in instances:
                file.write(f"( {os.path.splitext(instance.file.filename)[0]} \"{instance.transcription}\" )\n")

    @classmethod
    def output_help_text(cls) -> str:
        return "the filename of the FestVox file to write the annotations into"

    def expects_file(self) -> bool:
        return True

    def extract_file_info_from_external_format(self, instance: FestVoxFormat) -> AudioInfo:
        return instance.file
