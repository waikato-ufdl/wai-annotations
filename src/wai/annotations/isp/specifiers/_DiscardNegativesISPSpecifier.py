from typing import Type

from ...core.component import InlineStreamProcessor
from ...core.specifier import ISPSpecifier


class DiscardNegativesISPSpecifier(ISPSpecifier):
    """
    Specifies the discard-negatives ISP.
    """
    @classmethod
    def domains(cls) -> None:
        # Works for all domains
        return None

    @classmethod
    def processor_type(cls) -> Type[InlineStreamProcessor]:
        from ..discard_negatives import DiscardNegatives
        return DiscardNegatives

    @classmethod
    def description(cls) -> str:
        return "Discards negative examples (those without annotations) from the stream"
