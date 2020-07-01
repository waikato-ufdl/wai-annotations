from typing import Type

from ...core.component import InlineStreamProcessor
from ...core.specifier import ISPSpecifier


class DuplicateFileNamesISPSpecifier(ISPSpecifier):
    """
    Specifies the duplicate file-name discarder.
    """
    @classmethod
    def description(cls) -> str:
        return "Causes the conversion stream to halt when multiple dataset items " \
               "have the same filename"

    @classmethod
    def domains(cls) -> None:
        return None

    @classmethod
    def processor_type(cls) -> Type[InlineStreamProcessor]:
        from ..duplicate_filenames import DuplicateFileNameChecker
        return DuplicateFileNameChecker
