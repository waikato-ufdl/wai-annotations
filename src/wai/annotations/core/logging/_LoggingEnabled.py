import logging

from ._root_logger import ROOT_LOGGER_NAME


class LoggingEnabled:
    """
    Mixin class which adds logging support to the inheriting class.
    """
    # The name of the logger to use for the class.
    # Must be set by the class or logging will except
    logger_name: str = ""

    def get_logger(self) -> logging.Logger:
        """
        Gets the logger for the class.

        :return:    The logger.
        """
        # Make sure the name is a string
        if not isinstance(self.logger_name, str):
            raise TypeError(f"Logger name must be a string")

        # Make sure the name has been set correctly
        if not self.logger_name.startswith(ROOT_LOGGER_NAME):
            raise ValueError(f"Logger name ('{self.logger_name}') must be a child of the root logger "
                             f"(start with '{ROOT_LOGGER_NAME}.')")

        return logging.getLogger(self.logger_name)

    # The logger for the class
    logger: logging.Logger = property(get_logger)
