from argparse import Namespace
from typing import Iterable, Union, Any

from wai.common.cli import OptionsList

from ...core.component import InlineStreamProcessor
from ...core.instance import Instance


class DuplicateFileNameChecker(InlineStreamProcessor[Instance]):
    """
    Processes a stream of images ensuring that the same
    image name doesn't appear twice.
    """
    def __init__(self,
                 _namespace: Union[Namespace, OptionsList, None] = None,
                 **internal: Any):
        super().__init__(_namespace, **internal)
        self._seen_names = set()

    def _process_element(self, element: Instance) -> Iterable[Instance]:
        # Get the image name from the element
        image_name = element.file_info.filename

        # If we've seen it, raise an error
        if image_name in self._seen_names:
            raise ValueError(f"Image named '{image_name}' appeared multiple times during conversion")

        # Add the name to the set of seen images
        self._seen_names.add(image_name)

        return element,
