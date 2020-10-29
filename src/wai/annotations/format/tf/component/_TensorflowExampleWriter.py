import os
from os.path import join
from typing import List, Optional, Tuple, Iterator, ContextManager

from wai.common.cli.options import TypedOption

from ....core.component.util import (
    SplitSink,
    LocalFileWriter,
    WithPersistentSplitFiles,
    ExpectsFile
)
from ....core.stream.util import ProcessState
from ....core.util import InstanceState
from ..utils import (
    tensorflow as tf,
    LabelMapAccumulator,
    TensorflowExampleExternalFormat
)


class TensorflowExampleWriter(
    ExpectsFile,
    WithPersistentSplitFiles[List[tf.io.TFRecordWriter]],
    LocalFileWriter[Tuple[int, TensorflowExampleExternalFormat]],
    SplitSink[Tuple[int, TensorflowExampleExternalFormat]]
):
    """
    Writer of Tensorflow example records.
    """
    shards = TypedOption(
        "-s", "--shards",
        type=str,
        nargs="+",
        metavar="FILENAME",
        help="additional shards to write to"
    )

    protobuf_label_map = TypedOption(
        "-p", "--protobuf",
        type=str,
        metavar="FILENAME",
        help="for storing the label strings and IDs"
    )

    _num_writers: int = InstanceState(lambda self: len(self.shards) + 1)

    _label_map_accumulator: Optional[LabelMapAccumulator] = ProcessState(
        lambda self: None if self.protobuf_label_map is None else LabelMapAccumulator()
    )

    def consume_element_for_split(
            self,
            element: Tuple[int, TensorflowExampleExternalFormat]
    ):
        index, example = element

        if self._label_map_accumulator is not None:
            self._label_map_accumulator.accumulate(example)

        self._split_files[index % self._num_writers].write(example.SerializeToString())

    def finish_split(self):
        if self._label_map_accumulator is None:
            return

        # Write the accumulated labels
        self.write_protobuf_label_map(
            self._label_map_accumulator,
            self.get_split_path(self.split_label, self.output_path)
        )

    def write_protobuf_label_map(self, label_map_accumulator: LabelMapAccumulator, path: str):
        """
        Writes the label-to-index mapping to the given file, in
        protobuf format, if an output filename was given.
        """
        # Extract the label map and sort it
        labels_sorted = [
            (index, label)
            for label, index in label_map_accumulator.label_map.items()
        ]
        labels_sorted.sort(key=lambda entry: entry[0])

        # Format the label index map
        protobuf: List[str] = [
            "item {\n" +
            f"  id: {index}\n" +
            f"  name: '{label}'\n" +
            "}\n"
            for index, label in labels_sorted
        ]

        # Write the lines to the specified file
        with open(join(path, self.protobuf_label_map), 'w') as file:
            file.writelines(protobuf)

    @classmethod
    def get_help_text_for_output_option(cls) -> str:
        return "name of output file for TFRecords"

    def _init_split_files(self) -> List[tf.io.TFRecordWriter]:
        # Get the split path
        split_path = self.get_split_path(self.split_label, self.output, True)

        # Format the paths for the shards
        all_file_names = [split_path]
        for shard in self.shards:
            # Concatenate all output file-names
            all_file_names.append(
                os.path.join(
                    os.path.dirname(split_path),
                    shard
                )
            )

        # Open the output file for sharded writing
        return [tf.io.TFRecordWriter(file_name) for file_name in all_file_names]

    def _iterate_split_files(self, split_files: List[tf.io.TFRecordWriter]) -> Iterator[ContextManager]:
        return iter(split_files)
