from argparse import ArgumentParser, Namespace
from typing import Iterable, Dict, Any, Optional, List

import tensorflow as tf
import contextlib2

from ...core import Writer
from ...core.external_formats import TensorflowExampleExternalFormat
from ...tf_utils import extract_feature, open_sharded_output_tfrecords


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

        # The label map
        self._label_map: Dict[str, int] = {}

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

    def label_map_accumulator(self, instance: TensorflowExampleExternalFormat) -> TensorflowExampleExternalFormat:
        """
        Pass-through method which records the label mappings.

        :param instance:    An instance to process.
        """
        # Create a method to decode the binary strings
        def decode_utf_8(bytes_: bytes) -> str:
            return bytes_.decode("utf-8")

        # Get and decode the labels from the example
        labels: List[str] = list(map(decode_utf_8, extract_feature(instance.features, 'image/object/class/text')))

        # Get the classes from the example
        classes: List[int] = extract_feature(instance.features, 'image/object/class/label')

        # Make sure the labels and classes are the same size
        if len(labels) != len(classes):
            raise ValueError(f"Number of labels differs from number of classes")

        # Check and add labels/classes to the label map
        for label, class_ in zip(labels, classes):
            if label in self._label_map:
                if self._label_map[label] != class_:
                    raise RuntimeError(f"'{label}' maps to {self._label_map[label]} already but was "
                                       f"redefined to {class_}")
            else:
                self._label_map[label] = class_

        return instance

    def write(self, instances: Iterable[TensorflowExampleExternalFormat], path: str):
        # Reset the label map
        if self.protobuf_label_map is not None:
            self._label_map = {}
            instances = map(self.label_map_accumulator, instances)

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
        self.write_protobuf_label_map()

    def write_protobuf_label_map(self):
        """
        Writes the label-to-index mapping to the given file, in
        protobuf format, if an output filename was given.
        """
        # Abort if no file to write to
        if self.protobuf_label_map is None:
            return

        # Format the label index map
        protobuf: List[str] = ["item {\n" +
                               f"  id: {index}\n" +
                               f"  name: '{label}'\n" +
                               "}\n"
                               for label, index in self._label_map.items()]

        # Write the lines to the specified file
        with open(self.protobuf_label_map, 'w') as file:
            file.writelines(protobuf)
