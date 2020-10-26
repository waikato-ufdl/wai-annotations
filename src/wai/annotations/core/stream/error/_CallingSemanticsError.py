class CallingSemanticsError(Exception):
    """
    Error when the calling semantics of the 'then'/'done' functions
    are not followed by a stream-component.
    """
    def __init__(self, reason: str):
        super().__init__(reason)
