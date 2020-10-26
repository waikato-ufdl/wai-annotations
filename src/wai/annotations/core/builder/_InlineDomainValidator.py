from typing import Type, Tuple

from ..domain import Instance, DomainSpecifier
from ..stream import StreamProcessor, ThenFunction, DoneFunction
from ..stream.util import RequiresNoFinalisation
from .error import BadDomain


class InlineDomainValidator(
    RequiresNoFinalisation,
    StreamProcessor[Instance, Instance]
):
    """
    Makes sure all instances are from the specified domain.
    """
    def __init__(self, *domains: Type[DomainSpecifier]):
        self._domains: Tuple[Type[DomainSpecifier], ...] = domains
        self._instance_classes: Tuple[Type[Instance], ...] = tuple(domain.instance_type() for domain in domains)

    def process_element(
            self,
            element: Instance,
            then: ThenFunction[Instance],
            done: DoneFunction
    ):
        # Make sure the instance is from the given domain
        if not isinstance(element, self._instance_classes):
            raise BadDomain(f"{element.__class__.__name__} in stream where allowed domains are: "
                            f"{', '.join(domain.name() for domain in self._domains)}")

        then(element)
