class Classification:
    """
    Represents a categorical classification of the data.
    """
    def __init__(self, label: str):
        self._label: str = label

    @property
    def label(self) -> str:
        return self._label

    def __str__(self):
        return self._label
