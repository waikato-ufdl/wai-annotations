from typing import Iterable, Type, Tuple, TypeVar

from ..error import BadDomain
from ..specifier import DomainSpecifier
from ..stream import InlineStreamProcessor
from ..instance import Instance

InstanceType = TypeVar("InstanceType", bound=Instance)


class InlineDomainValidator(InlineStreamProcessor[Instance]):
    """
    Makes sure all instances are from the specified domain.
    """
    def __init__(self, *domains: DomainSpecifier):
        self._instance_classes: Tuple[Type[Instance], ...] = tuple(domain.instance_class() for domain in domains)

    def _process_element(self, element: InstanceType) -> Iterable[InstanceType]:
        # Make sure the instance is from the given domain
        if not isinstance(element, self._instance_classes):
            raise BadDomain()

        return element,
