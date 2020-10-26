class Transcription:
    """
    The transcription of a piece of recorded speech.
    """
    def __init__(self, text: str):
        self._text: str = text

    @property
    def text(self) -> str:
        """
        Gets the text of the transcription.
        """
        return self._text

    def __str__(self) -> str:
        return self._text
