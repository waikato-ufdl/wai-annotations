class InputStageNotFirst(Exception):
    """
    Error for when trying to add an input stage to a conversion
    anywhere but as the first stage.
    """
    def __init__(self):
        super().__init__("Attempted to add an input stage in a position other than "
                         "first in the conversion chain.")
