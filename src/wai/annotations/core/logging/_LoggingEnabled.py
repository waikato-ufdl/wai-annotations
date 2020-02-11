import logging
from typing import Optional

from ._root_logger import ROOT_LOGGER_NAME


class LoggingEnabled:
    """
    Mixin class which adds logging support to the inheriting class.
    """
    # The cached logger
    _logger: Optional[logging.Logger] = None

    @property
    def logger(self) -> logging.Logger:
        """
        Gets the logger for the class.

        :return:    The logger.
        """
        return self._logger

    def __init_subclass__(cls, **kwargs):
        super().__init_subclass__(**kwargs)

        # Only classes in the wai.annotations namespace can use this mixin
        if not cls.__module__.startswith(f"{ROOT_LOGGER_NAME}."):
            raise TypeError(f"Only classes in the '{ROOT_LOGGER_NAME}' namespace "
                            f"can use the {LoggingEnabled.__name__} mixin class")

        # Cache the logger
        cls._logger = logging.getLogger(cls.__module__ + "." + cls.__name__)
