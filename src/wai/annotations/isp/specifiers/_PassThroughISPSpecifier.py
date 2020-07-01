from typing import Type

from ...core.component import InlineStreamProcessor
from ...core.specifier import ISPSpecifier


class PassThroughISPSpecifier(ISPSpecifier):
    """
    Specifier for the pass-through inline stream-processor.
    """
    @classmethod
    def description(cls) -> str:
        return "Dummy ISP which has no effect on the conversion stream"

    @classmethod
    def domains(cls) -> None:
        # Passthrough works in any domain
        return None

    @classmethod
    def processor_type(cls) -> Type[InlineStreamProcessor]:
        from ..passthrough import PassThrough
        return PassThrough
