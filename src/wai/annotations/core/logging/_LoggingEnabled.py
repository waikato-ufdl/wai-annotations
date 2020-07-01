import logging
from typing import Optional


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

    @classmethod
    def get_class_logger(cls) -> logging.Logger:
        """
        Gets the logger for the class.

        :return:    The logger.
        """
        return cls._logger

    def __init_subclass__(cls, **kwargs):
        super().__init_subclass__(**kwargs)

        # Cache the logger
        cls._logger = logging.getLogger(cls.__module__ + "." + cls.__name__)
