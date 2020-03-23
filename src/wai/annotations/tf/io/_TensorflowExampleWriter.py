from os.path import dirname, join
from typing import Iterable, List

import contextlib2

from wai.common.cli.options import TypedOption

from ...core import ImageInfo
from ...core.components import Writer
from .._ensure_available import tensorflow as tf
from ..utils import image_info_from_example, LabelMapAccumulator, open_sharded_output_tfrecords
from .._format import TensorflowExampleExternalFormat


class TensorflowExampleWriter(Writer[TensorflowExampleExternalFormat]):
    """
    Writer of Tensorflow example records.
    """
    shards = TypedOption("-s", "--shards",
                         metavar="num", required=False, type=int,
                         help="number of shards to split the images into")
    protobuf_label_map = TypedOption("-p", "--protobuf",
                                     metavar="file", required=False, type=str,
                                     help="for storing the label strings and IDs")

    def write(self, instances: Iterable[TensorflowExampleExternalFormat], path: str):
        # Reset the label map
        label_map_accumulator = None
        if self.protobuf_label_map is not None:
            label_map_accumulator = LabelMapAccumulator()
            instances = label_map_accumulator.process(instances)

        # Sharded writing
        if self.shards is not None and self.shards > 1:
            with contextlib2.ExitStack() as exit_stack:
                # Open the output file for sharded writing
                writers = open_sharded_output_tfrecords(exit_stack, path, self.shards)

                for index, instance in enumerate(instances):
                    writers[index % self.shards].write(instance.SerializeToString())

        # Unsharded writing
        else:
            # Write each instance
            with tf.io.TFRecordWriter(path) as writer:
                for instance in instances:
                    writer.write(instance.SerializeToString())

        # Write out the label map as well
        if label_map_accumulator is not None:
            self.write_protobuf_label_map(label_map_accumulator, path)

    def write_protobuf_label_map(self, label_map_accumulator: LabelMapAccumulator, path: str):
        """
        Writes the label-to-index mapping to the given file, in
        protobuf format, if an output filename was given.
        """
        # Format the label index map
        protobuf: List[str] = ["item {\n" +
                               f"  id: {index}\n" +
                               f"  name: '{label}'\n" +
                               "}\n"
                               for label, index in label_map_accumulator.label_map.items()]

        # Write the lines to the specified file
        with open(join(dirname(path), self.protobuf_label_map), 'w') as file:
            file.writelines(protobuf)

    def extract_image_info_from_external_format(self, instance: TensorflowExampleExternalFormat) -> ImageInfo:
        return image_info_from_example(instance)

    def expects_file(self) -> bool:
        return True

    @classmethod
    def output_help_text(cls) -> str:
        return "name of output file for TFRecords"
