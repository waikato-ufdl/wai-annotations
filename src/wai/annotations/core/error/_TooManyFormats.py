class TooManyFormats(Exception):
    """
    Error for when a conversion chain tries to add too many
    format specifiers (can have at most one input format and
    one output format).
    """
    def __init__(self):
        super().__init__("Attempted to add too many format specifiers to the conversion chain. "
                         "Can have at most one input format and one output format. Perhaps "
                         "you tried to add the input format after an ISP was specified?")
