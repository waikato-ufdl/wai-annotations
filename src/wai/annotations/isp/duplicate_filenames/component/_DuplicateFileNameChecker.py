from typing import Set

from ....core.component import ProcessorComponent
from ....core.stream import ThenFunction, DoneFunction
from ....core.stream.util import RequiresNoFinalisation, ProcessState
from ....core.domain import Instance


class DuplicateFileNameChecker(
    RequiresNoFinalisation,
    ProcessorComponent[Instance, Instance]
):
    """
    Processes a stream of images ensuring that the same
    image name doesn't appear twice.
    """
    # The set of file-names we've already seen
    _seen_names: Set[str] = ProcessState(lambda self: set())

    def process_element(
            self,
            element: Instance,
            then: ThenFunction[Instance],
            done: DoneFunction
    ):
        # Get the image name from the element
        image_name = element.data.filename

        # If we've seen it, raise an error
        if image_name in self._seen_names:
            raise ValueError(f"Image named '{image_name}' appeared multiple times during conversion")

        # Add the name to the set of seen images
        self._seen_names.add(image_name)

        then(element)
