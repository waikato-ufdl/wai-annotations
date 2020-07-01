class UnknownPluginName(Exception):
    """
    Exception for when a plugin is selected by a name that
    is not known to the plugin system.
    """
    def __init__(self, name: str):
        super().__init__(f"No plugin named '{name}'")
