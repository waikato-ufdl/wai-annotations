from ....core.component import ProcessorComponent
from ....core.domain import Instance
from ....core.stream import ThenFunction, DoneFunction
from ....core.stream.util import RequiresNoFinalisation


class DiscardNegatives(
    RequiresNoFinalisation,
    ProcessorComponent[Instance, Instance]
):
    """
    ISP which removes negatives from the stream.
    """
    def process_element(
            self,
            element: Instance,
            then: ThenFunction[Instance],
            done: DoneFunction
    ):
        if not element.is_negative:
            then(element)
