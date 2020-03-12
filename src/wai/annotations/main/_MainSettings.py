from logging import WARNING, INFO, DEBUG

from wai.common import ClassRegistry
from wai.common.cli import CLIInstantiable
from wai.common.cli.options import CountOption, ClassOption
from wai.common.cli.util import TranslationTable

from ..core.coercions import MaskBoundsCoercion, BoxBoundsCoercion


class MainSettings(CLIInstantiable):
    """
    The main settings class for the library. Contains global
    settings.
    """
    # The verbosity of logging to implement
    VERBOSITY = CountOption(
        "-v",
        translation=TranslationTable(WARNING, INFO, DEBUG),
        help="whether to be more verbose when generating the records"
    )

    # The coercion to apply to annotations
    COERCION = ClassOption(
        "-f", "--force",
        registry=ClassRegistry().alias(MaskBoundsCoercion, "mask").alias(BoxBoundsCoercion, "bbox"),
        help="forces located objects into a particular boundary type"
    )
