"""
Package for utility functions for working with the object detection domain.
"""
from ._metadata import (
    object_has_label,
    get_object_label,
    set_object_label,
    object_has_prefix,
    get_object_prefix,
    set_object_prefix,
    get_object_metadata,
    set_object_metadata
)
from ._polygon_from_rectangle import polygon_from_rectangle
from ._render_annotations_onto_image import render_annotations_onto_image
