from typing import Type, Set, Optional

from ...domain import DomainSpecifier


class StageInvalidForDomains(Exception):
    """
    Error for when an attempt is made to add a stage to the
    conversion pipeline which doesn't handle any of the domains
    it might receive.
    """
    def __init__(self, current_domains: Set[Type[DomainSpecifier]], reason: Optional[str] = None):
        full_reason = "Attempted to add stage which cannot handle domains {"
        full_reason += ", ".join(domain.name() for domain in current_domains)
        full_reason += "]"
        if reason is not None:
            full_reason += ": " + reason

        super().__init__(full_reason)
