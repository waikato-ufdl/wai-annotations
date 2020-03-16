from pkg_resources import EntryPoint

from ....core import FormatSpecifier
from ..constants import FORMATS_ENTRY_POINT_GROUP


class BadFormatSpecifier(Exception):
    """
    Error for when a format-specifier entry-point is incorrectly configured.
    """
    def __init__(self):
        super().__init__(f"Entry points in the '{FORMATS_ENTRY_POINT_GROUP}' group should "
                         f"be callables that take no arguments are return a {FormatSpecifier.__name__} "
                         f"instance")

    @staticmethod
    def load_from_entry_point(entry_point: EntryPoint) -> FormatSpecifier:
        """
        Loads a format-specifier from an entry-point, or raises
        an instance of this error if it can't.

        :param entry_point:     The entry-point to load from.
        :return:                The format specifier.
        """
        # Make sure all escaping exceptions are of this type
        try:
            # Load the target of the entry-point
            format_specifier_function = entry_point.load()

            # Should be callable
            if not callable(format_specifier_function):
                raise BadFormatSpecifier()

            # Call the function to get the specifier
            format_specifier = format_specifier_function()

            # Make sure it is a format specifier
            if not isinstance(format_specifier, FormatSpecifier):
                raise BadFormatSpecifier()

            return format_specifier

        # If we raised an instance, let it escape
        except BadFormatSpecifier:
            raise

        # Wrap any other error as an instance
        except Exception as e:
            raise BadFormatSpecifier() from e
