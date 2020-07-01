import os
from abc import abstractmethod
from typing import Optional


class FileInfo:
    """
    The base class for representing a single item in a data-set, without
    its annotations. Should be sub-typed by specific domains to represent
    items in that domain, e.g. image files for the image domain.
    """
    def __init__(self,
                 filename: str,
                 data: Optional[bytes] = None):
        self._filename: str = filename
        self._data: Optional[bytes] = data

    @property
    def filename(self) -> str:
        """
        The filename of the file.
        """
        return self._filename

    @property
    def data(self) -> Optional[bytes]:
        """
        The binary contents of the file, if available.
        """
        return self._data

    @classmethod
    def from_file(cls, filepath: str) -> 'FileInfo':
        """
        Reads an item from disk.

        :param filepath:    The file to read.
        :return:            The file-info object.
        """
        # Try to read the data
        data = None
        if os.path.exists(filepath):
            with open(filepath, "rb") as file:
                data = file.read()

        # Trim the filename
        filename = os.path.basename(filepath)

        return cls.from_file_data(filename, data)

    @classmethod
    @abstractmethod
    def from_file_data(cls, file_name: str, file_data: bytes) -> 'FileInfo':
        """
        Creates an instance of this type from just the filename and
        binary file data.

        :param file_name:   The filename.
        :param file_data:   The file-data.
        :return:            A FileInfo instance.
        """
        pass

    def write_data_if_present(self, path: str) -> bool:
        """
        Writes the file data to disk under its filename in the given path.

        :param path:    The directory to write the file into.
        :return:        Whether the file was written or not.
        """
        # Can't write anything without data
        if self._data is None:
            return False

        # Write the data to disk
        with open(os.path.join(path, self._filename), "wb") as file:
            file.write(self._data)

        return True
