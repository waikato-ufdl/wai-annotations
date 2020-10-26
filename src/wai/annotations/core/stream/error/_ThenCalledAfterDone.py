from ._CallingSemanticsError import CallingSemanticsError


class ThenCalledAfterDone(CallingSemanticsError):
    """
    Error for when a stream-component calls 'then' after it
    has already called 'done'.
    """
    def __init__(self):
        super().__init__("'then' function called after 'done'")
