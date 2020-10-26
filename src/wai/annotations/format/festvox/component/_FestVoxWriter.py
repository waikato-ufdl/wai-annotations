import os
from typing import Iterable, IO, ContextManager

from ....core.component.util import (
    SeparateFileWriter,
    SplitSink,
    RequiresNoSplitFinalisation,
    WithPersistentSplitFiles,
    SplitState,
    ExpectsFile
)
from ....domain.audio.speech import SpeechInstance


class FestVoxWriter(
    ExpectsFile,
    WithPersistentSplitFiles[IO[str]],
    RequiresNoSplitFinalisation,
    SeparateFileWriter[SpeechInstance],
    SplitSink[SpeechInstance]
):
    """
    Writer of the Festival FestVox speech annotation format.
    """
    _split_path: str = SplitState(lambda self: self.get_split_path(self.split_label, self.output_path))

    def consume_element_for_split(self, element: SpeechInstance):
        # Write the audio file
        self.write_data_file(element.data, self._split_path)

        # If there's no transcription, we're done
        if element.annotations is None:
            return

        # Write the transcription to the festvox file
        self._split_files.write(
            f"( {os.path.splitext(element.data.filename)[0]} \"{element.annotations.text}\" )\n"
        )

    @classmethod
    def get_help_text_for_output_option(cls) -> str:
        return "the filename of the FestVox file to write the annotations into"

    def _init_split_files(self) -> IO[str]:
        return open(self.get_split_path(self.split_label, self.output, True), "w")

    def _iterate_split_files(self, split_files: IO[str]) -> Iterable[ContextManager]:
        return split_files,
