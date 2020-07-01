from typing import Iterable, List, Dict

from ....core.stream import InlineStreamProcessor
from .._format import TensorflowExampleExternalFormat
from ._extract_feature import extract_feature


class LabelMapAccumulator(InlineStreamProcessor[TensorflowExampleExternalFormat]):
    """
    Accumulates a label map from the passing Tensorflow examples.
    """
    # Property to get the label map
    label_map = property(lambda self: self._label_map.copy())

    def __init__(self):
        # The accumulated label map
        self._label_map: Dict[str, int] = {}

    def _process_element(self, element: TensorflowExampleExternalFormat) -> Iterable[TensorflowExampleExternalFormat]:
        # Create a method to decode the binary strings
        def decode_utf_8(bytes_: bytes) -> str:
            return bytes_.decode("utf-8")

        # Get and decode the labels from the example
        labels: List[str] = list(map(decode_utf_8, extract_feature(element.features, 'image/object/class/text')))

        # Get the classes from the example
        classes: List[int] = extract_feature(element.features, 'image/object/class/label')

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

        return element,
