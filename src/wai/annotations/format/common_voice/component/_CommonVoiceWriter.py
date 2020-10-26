import csv
from typing import IO, ContextManager, Iterable


from ....core.component.util import (
    SeparateFileWriter,
    SplitSink,
    SplitState,
    RequiresNoSplitFinalisation,
    WithPersistentSplitFiles,
    ExpectsFile
)
from ....domain.audio.speech import SpeechInstance
from ..util import CommonVoiceDialect, EXPECTED_HEADER

EXPECTED_HEADER_LIST = EXPECTED_HEADER.split('\t')


class CommonVoiceWriter(
    ExpectsFile,
    WithPersistentSplitFiles[IO[str]],
    RequiresNoSplitFinalisation,
    SeparateFileWriter[SpeechInstance],
    SplitSink[SpeechInstance]
):
    """
    Writer of Mozilla's CommonVoice speech annotation format.
    """
    _split_path: str = SplitState(lambda self: self.get_split_path(self.split_label, self.output_path))

    # The TSV writer writing to the file for the current split
    split_writer: csv.DictWriter = SplitState(lambda self: self._init_tsv_writer())

    def consume_element_for_split(
            self,
            element: SpeechInstance
    ):
        # Write the audio file to the split directory
        self.write_data_file(element.data, self._split_path)

        # We're done if this is a negative
        if element.annotations is None:
            return

        # Create the CommonVoice TSV row as a dictionary
        instance_dict = {
            "client_id": "",
            "path": element.data.filename,
            "sentence": element.annotations.text,
            "up_votes": 0,
            "down_votes": 0,
            "age": None,
            "gender": None,
            "accent": None,
            "locale": "",
            "segment": ""
        }

        # Write the instance to the file
        self.split_writer.writerow(instance_dict)

    @classmethod
    def get_help_text_for_output_option(cls) -> str:
        return "the filename of the TSV file to write the annotations into"

    def _init_split_files(self) -> IO[str]:
        return open(self.get_split_path(self.split_label, self.output, True), 'w')

    def _iterate_split_files(self, split_files: IO[str]) -> Iterable[ContextManager]:
        return split_files,

    def _init_tsv_writer(self) -> csv.DictWriter:
        # Create a TSV writer using the header
        csv_writer = csv.DictWriter(self._split_files, EXPECTED_HEADER_LIST, dialect=CommonVoiceDialect)

        # Write the header to file
        csv_writer.writeheader()

        return csv_writer
