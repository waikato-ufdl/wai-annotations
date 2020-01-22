import logging
from typing import Optional

from ._root_logger import ROOT_LOGGER_NAME


class LoggingEnabled:
    """
    Mixin class which adds logging support to the inheriting class.
    """
    # The name of the logger to use for the class.
    # Must be set by the class or logging will except
    logger_name: str = ""

    # The cached logger
    __logger: Optional[logging.Logger] = None

    @classmethod
    def logger(cls) -> logging.Logger:
        """
        Gets the logger for the class.

        :return:    The logger.
        """
        if cls.__logger is None:
            # Make sure the name is a string
            if not isinstance(cls.logger_name, str):
                raise TypeError(f"Logger name must be a string")

            # Make sure the name has been set correctly
            if not cls.logger_name.startswith(ROOT_LOGGER_NAME):
                raise ValueError(f"Logger name ('{cls.logger_name}') must be a child of the root logger "
                                 f"(start with '{ROOT_LOGGER_NAME}.')")

            cls.__logger = logging.getLogger(cls.logger_name)

        return cls.__logger
