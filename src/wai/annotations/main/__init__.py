"""
Package containing the functionality required for running wai.annotations
as an application.
"""
from ._help import format_help, list_plugins, help_plugins, filter_plugins
from ._main import main, sys_main
from ._MainSettings import MainSettings
