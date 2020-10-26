from typing import Type, Tuple

from ....core.component import ProcessorComponent
from ....core.domain import DomainSpecifier
from ....core.specifier import ProcessorStageSpecifier


class DuplicateFileNamesISPSpecifier(ProcessorStageSpecifier):
    """
    Specifies the duplicate file-name discarder.
    """
    @classmethod
    def description(cls) -> str:
        return "Causes the conversion stream to halt when multiple dataset items " \
               "have the same filename"

    @classmethod
    def domain_transfer_function(
            cls,
            input_domain: Type[DomainSpecifier]
    ) -> Type[DomainSpecifier]:
        # Works in any domain
        return input_domain

    @classmethod
    def components(cls) -> Tuple[Type[ProcessorComponent]]:
        from ...duplicate_filenames.component import DuplicateFileNameChecker
        return DuplicateFileNameChecker,
