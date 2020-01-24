"""
Package for general utility functions.
"""
from ._chain_map import chain_map
from ._extension_to_regex import extension_to_regex
from ._get_associated_image import get_associated_image
from ._get_files_from_directory import get_files_from_directory
from ._get_image_size import get_image_size
from ._metadata import (
    get_object_label,
    set_object_label,
    get_object_prefix,
    set_object_prefix,
    get_object_metadata,
    set_object_metadata
)
from ._read_file_list import read_file_list
from ._recursive_iglob import recursive_iglob
