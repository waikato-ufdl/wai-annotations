class StageAfterOutput(Exception):
    """
    Error for when a conversion stage is added after the output format.
    """
    def __init__(self):
        super().__init__("Attempted to add a conversion stage after output format already set")
