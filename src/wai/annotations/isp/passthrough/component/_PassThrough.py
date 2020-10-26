from ....core.component import ProcessorComponent
from ....core.domain import Instance
from ....core.stream import ThenFunction, DoneFunction
from ....core.stream.util import RequiresNoFinalisation


class PassThrough(
    RequiresNoFinalisation,
    ProcessorComponent[Instance, Instance]
):
    """
    Inline stream-processor which does nothing to the stream.
    """
    def process_element(
            self,
            element: Instance,
            then: ThenFunction[Instance],
            done: DoneFunction
    ):
        then(element)
