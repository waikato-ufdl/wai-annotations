"""
Provides the application logger for wai.annotations.
"""
from logging import Logger, DEBUG
import os

from wai.common.logging import create_standard_application_root_logger, DEBUG_HANDLER_NAME

# Setup logging
_logger = create_standard_application_root_logger()

# Remove the PIL logging from the debug logger
for handler in _logger.handlers:
    if handler.name == DEBUG_HANDLER_NAME:
        handler.addFilter(lambda record: record.name != 'PIL.PngImagePlugin')

# Capture all log events by default, unless an environment variable is set
_logger.level = int(os.getenv("WAIANN_LOG_LEVEL", str(DEBUG)))


def get_app_logger() -> Logger:
    """
    Gets the root application logger for wai.annotations.
    """
    return _logger
