from argparse import ArgumentParser, Namespace
from typing import Iterable, Dict, Any, Optional, List

import tensorflow as tf
import contextlib2

from ...core import Writer
from ...core.external_formats import TensorflowExampleExternalFormat
from ...tf_utils import LabelMapAccumulator, open_sharded_output_tfrecords


class TensorflowExampleWriter(Writer[TensorflowExampleExternalFormat]):
    """
    Writer of Tensorflow example records.
    """
    def __init__(self, output: str, shards: int = 1, protobuf_label_map: Optional[str] = None):
        super().__init__(output)

        # The number of shards to use for sharded output
        # (<= 1 means unsharded output)
        self.shards: int = shards

        # The name of the file to write the label map to
        # (in protobuf format)
        self.protobuf_label_map: Optional[str] = protobuf_label_map

    @classmethod
    def configure_parser(cls, parser: ArgumentParser):
        super().configure_parser(parser)

        parser.add_argument(
            "-s", "--shards", metavar="num", dest="shards", required=False, type=int,
            help="number of shards to split the images into (<= 1 for off)", default=-1)

        parser.add_argument(
            "-p", "--protobuf", metavar="file", dest="protobuf_label_map", required=False,
            help="for storing the label strings and IDs", default=None)

    @classmethod
    def determine_kwargs_from_namespace(cls, namespace: Namespace) -> Dict[str, Any]:
        kwargs = super().determine_kwargs_from_namespace(namespace)
        kwargs.update(shards=namespace.shards,
                      protobuf_label_map=namespace.protobuf_label_map)
        return kwargs

    @classmethod
    def output_help_text(cls) -> str:
        return "name of output file for TFRecords"

    def write(self, instances: Iterable[TensorflowExampleExternalFormat], path: str):
        # Reset the label map
        label_map_accumulator = None
        if self.protobuf_label_map is not None:
            label_map_accumulator = LabelMapAccumulator()
            instances = label_map_accumulator.process(instances)

        # Sharded writing
        if self.shards > 1:
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
            self.write_protobuf_label_map(label_map_accumulator)

    def write_protobuf_label_map(self, label_map_accumulator: LabelMapAccumulator):
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
        with open(self.protobuf_label_map, 'w') as file:
            file.writelines(protobuf)
