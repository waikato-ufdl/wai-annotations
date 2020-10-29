from ....core.component import ProcessorComponent
from ....core.domain import Instance
from ....core.stream import ThenFunction, DoneFunction
from ....core.stream.util import RequiresNoFinalisation


class StripAnnotations(
    RequiresNoFinalisation,
    ProcessorComponent[Instance, Instance]
):
    """
    Inline stream-processor which removes annotations from the stream.
    """
    def process_element(
            self,
            element: Instance,
            then: ThenFunction[Instance],
            done: DoneFunction
    ):
        then(
            type(element)(
                element.data,
                None
            )
        )
