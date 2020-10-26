from typing import Type

from ...domain import DomainSpecifier


class StageInvalidForDomain(Exception):
    """
    Error for when an attempt is made to add a stage to the
    conversion pipeline which doesn't handle the domain it will
    receive.
    """
    def __init__(self, current_domain: Type[DomainSpecifier], reason: str):
        super().__init__(f"Attempted to add stage which cannot handle "
                         f"{current_domain.name()}: {reason}")
