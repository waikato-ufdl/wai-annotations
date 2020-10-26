from abc import ABC
from typing import TypeVar, Optional

from wai.common.cli.options import FlagOption, Option

from ._SeparateFileWriter import SeparateFileWriter

ExternalFormat = TypeVar("ExternalFormat")


class JSONFileWriter(SeparateFileWriter[ExternalFormat], ABC):
    """
    Base class for writers that write their annotations out as a single JSON file.
    """
    pretty = FlagOption(
        "--pretty"
    )

    @property
    def indent(self) -> Optional[int]:
        """
        The level of indentation to use when writing the JSON file.
        """
        return 2 if self.pretty else None

    @classmethod
    def get_help_text_for_option(cls, option: Option) -> Optional[str]:
        if option is cls.pretty:
            return cls.get_help_text_for_pretty_option()
        return super().get_help_text_for_option(option)

    @classmethod
    def get_help_text_for_pretty_option(cls) -> str:
        """

        :return:
        """
        return "whether to format the JSON annotations file with indentation"
