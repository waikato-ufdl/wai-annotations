"""
Package of utilities for working with the ROI format.
"""
from ._combine_dicts import combine_dicts
from ._min_rect_from_roi_polygon import min_rect_from_roi_polygon
from ._polygon_from_roi_object import polygon_from_roi_object
from ._filenames import (
    roi_filename_for_image,
    get_associated_image_from_filename,
    handle_fix_defaults
)
from ._roi_polygon import roi_polygon