from ...core.instance import FileInfo


class AudioInfo(FileInfo):
    """
    Contains the information about an audio file.

    TODO: To match ImageInfo, implement the following:
          - Add format information (MP3, WAV, etc.) + property to read
          - Add run-time information (minutes and seconds) + property to read
          - Add conversion between formats
          - Add __get_attribute__ representations for Jupyter notebook widgets
    """
    @classmethod
    def from_file_data(cls, file_name: str, file_data: bytes) -> 'AudioInfo':
        return cls(file_name, file_data)
