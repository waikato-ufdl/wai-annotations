from ._CallingSemanticsError import CallingSemanticsError


class DoneNeverCalled(CallingSemanticsError):
    """
    Error for when a stream-component doesn't call 'done' during
    its processing lifetime.
    """
    def __init__(self):
        super().__init__("The 'done' function was never called")
