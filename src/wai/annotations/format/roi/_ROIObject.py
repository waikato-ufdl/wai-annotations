from typing import Dict, List, Optional

from wai.common.geometry import Polygon, Point

from ...core.logging import LoggingEnabled
from .utils import normalisation_constant_multi


class ROIObject(LoggingEnabled):
    """
    Holds a detected object from a ROI file.
    """
    # The ordered required position keywords for corner mode
    required_position_keywords_corner_mode = ("x0", "y0", "x1", "y1", "x0n", "y0n", "x1n", "y1n")

    # The ordered required position keywords for corner mode
    required_position_keywords_size_mode = ("x", "y", "w", "h", "xn", "yn", "wn", "hn")

    # The ordered required arguments to ROIObject
    required_other_keywords = ("label", "label_str", "score")

    # The ordered optional arguments to ROIObject
    optional_keywords = ("poly_x", "poly_y", "poly_xn", "poly_yn", "minrect_w", "minrect_h")

    def __init__(self,
                 x0: float, y0: float, x1: float, y1: float,
                 x0n: float, y0n: float, x1n: float, y1n: float,
                 label: int, label_str: str, score: float,
                 poly_x: Optional[List[float]] = None, poly_y: Optional[List[float]] = None,
                 poly_xn: Optional[List[float]] = None, poly_yn: Optional[List[float]] = None,
                 minrect_w: Optional[float] = None, minrect_h: Optional[float] = None,
                 **non_standard_kwargs):
        self.x0: float = x0
        self.y0: float = y0
        self.x1: float = x1
        self.y1: float = y1
        self.x0n: float = x0n
        self.y0n: float = y0n
        self.x1n: float = x1n
        self.y1n: float = y1n
        self.label: int = label
        self.label_str: str = label_str
        self.score: float = score
        self.poly_x: Optional[List[float]] = poly_x
        self.poly_y: Optional[List[float]] = poly_y
        self.poly_xn: Optional[List[float]] = poly_xn
        self.poly_yn: Optional[List[float]] = poly_yn
        self.minrect_w: Optional[float] = minrect_w
        self.minrect_h: Optional[float] = minrect_h

        # Capture any additional columns
        self.non_standard_kwargs = non_standard_kwargs

        # "file" is a reserved keyword for the ROI file format
        if "file" in non_standard_kwargs:
            raise NameError(f"'file' is reserved for the ROI file format, can't be in the non-standard keywords")

        # Make sure all of the polygon lists are the same length
        self.ensure_polygon_list_lengths()

    @property
    def x(self) -> float:
        return self.x0

    @property
    def y(self) -> float:
        return self.y0

    @property
    def w(self) -> float:
        return self.x1 - self.x0 + 1

    @property
    def h(self) -> float:
        return self.y1 - self.y0 + 1

    @property
    def xn(self) -> float:
        return self.x / self.image_width()

    @property
    def yn(self) -> float:
        return self.y / self.image_height()

    @property
    def wn(self) -> float:
        return self.w / self.image_width()

    @property
    def hn(self) -> float:
        return self.h / self.image_height()

    def ensure_polygon_list_lengths(self):
        """
        Makes sure all polygon lists match in length.
        """
        # Get the length of each list
        len_x = -1 if self.poly_x is None else len(self.poly_x)
        len_y = -1 if self.poly_y is None else len(self.poly_y)
        len_xn = -1 if self.poly_xn is None else len(self.poly_xn)
        len_yn = -1 if self.poly_yn is None else len(self.poly_yn)

        # Make sure all lengths are the same
        if len_x != len_y or len_y != len_xn or len_xn != len_yn:
            raise ValueError("Polygon lists have differing lengths")

    def has_polygon(self) -> bool:
        """
        Whether this ROI object has a polygon.

        :return:    True if the object has a polygon.
        """
        return self.poly_x is not None

    def polygon(self) -> Polygon:
        """
        Generates a polygon from the given ROI object.

        :return:            The polygon.
        """
        # Make sure the ROI object has a polygon
        if not self.has_polygon():
            raise ValueError(f"ROI object has no polygon")

        return Polygon(*(Point(round(x), round(y)) for x, y in zip(self.poly_x, self.poly_y)))

    def image_width(self) -> int:
        """
        Calculates the source image's width.

        :return:    The source image's width.
        """
        return normalisation_constant_multi(self.x0, self.x0n, self.x1, self.x1n)

    def image_height(self) -> int:
        """
        Calculates the source image's height.

        :return:    The source image's height.
        """
        return normalisation_constant_multi(self.y0, self.y0n, self.y1, self.y1n)

    @classmethod
    def required_keywords(cls, size_mode: bool):
        return (
                (cls.required_position_keywords_size_mode if size_mode else cls.required_position_keywords_corner_mode)
                + cls.required_other_keywords
        )

    @classmethod
    def keywords(cls, size_mode: bool):
        return cls.required_keywords(size_mode) + cls.optional_keywords

    def as_dict(self, size_mode: bool = False) -> Dict[str, str]:
        """
        Gets a dictionary representation of this object.

        :param size_mode:   Whether to export as a size-mode dictionary instead.
        :return:            A dict.
        """
        # Create a result dict
        result = {}

        # Get the keywords we expect to export
        keywords = self.keywords(size_mode)

        # Process each keyword in turn
        for keyword in keywords:
            # Get the value for the attribute
            value = getattr(self, keyword)

            # Ignore missing optional attributes
            if value is None:
                continue

            # Format the polygon lists as strings
            if isinstance(value, list):
                value = ",".join(map(str, value))

            # Add the string representation of the value to the dict
            result[keyword] = value

        result.update(**self.non_standard_kwargs)

        return result

    @classmethod
    def from_dict(cls, roi_dict: Dict[str, str]) -> "ROIObject":
        """
        Creates an object instance from the given dictionary.

        :param roi_dict:    The dict.
        :return:            A ROIObject instance.
        """
        # Create a set of keyword arguments
        kwargs = {}

        # Process each dictionary item in turn
        for keyword, value in roi_dict.items():
            # Ignore the file keyword
            if keyword == "file":
                continue

            # Add the value to the kwargs
            kwargs[keyword] = cls._parse(keyword, value)

        # If it's a size-mode dict, convert to a corner-mode one
        if "x" in kwargs:
            kwargs = cls._convert_size_mode_kwargs(**kwargs)

        return ROIObject(**kwargs)

    @classmethod
    def _parse(cls, keyword: str, value: str):
        """
        Parses the string representation of a value to its internal type.

        :param keyword: The name of the attribute.
        :param value:   The string representation of the attribute's value.
        """
        # Float types
        if keyword in {"x0", "y0", "x1", "y1", "x0n", "y0n", "x1n", "y1n",
                       "x", "y", "w", "h", "xn", "yn", "wn", "hn",
                       "score", "minrect_w", "minrect_h"}:
            return float(value) if value is not "" else None

        # Int types
        if keyword in {"label"}:
            return int(value)

        # List of float types
        if keyword in {"poly_x", "poly_y", "poly_xn", "poly_yn"}:
            return list(map(float, value.split(","))) if value is not "" else None

        # All other attributes are strings
        return value

    @classmethod
    def _convert_size_mode_kwargs(cls, **kwargs) -> Dict:
        """
        Converts the keyword arguments to the constructor from
        size-mode to the equivalent corner-mode dictionary.

        :param kwargs:  The size-mode keyword arguments.
        :return:        The corner-mode keyword arguments.
        """
        # Remove the size-mode arguments
        size_mode_kwargs = {}
        for keyword in cls.required_position_keywords_size_mode:
            size_mode_kwargs[keyword] = kwargs.pop(keyword)

        # Calculate the image's width/height for normalisation
        image_width = normalisation_constant_multi(size_mode_kwargs['x'],
                                                   size_mode_kwargs['xn'],
                                                   size_mode_kwargs['w'],
                                                   size_mode_kwargs['wn'])
        image_height = normalisation_constant_multi(size_mode_kwargs['y'],
                                                    size_mode_kwargs['yn'],
                                                    size_mode_kwargs['h'],
                                                    size_mode_kwargs['hn'])

        # Introduce the corner-mode equivalent arguments
        kwargs['x0'] = size_mode_kwargs['x']
        kwargs['y0'] = size_mode_kwargs['y']
        kwargs['x1'] = size_mode_kwargs['x'] + size_mode_kwargs['w'] - 1
        kwargs['y1'] = size_mode_kwargs['y'] + size_mode_kwargs['h'] - 1
        kwargs['x0n'] = kwargs['x0'] / image_width
        kwargs['y0n'] = kwargs['y0'] / image_height
        kwargs['x1n'] = kwargs['x1'] / image_width
        kwargs['y1n'] = kwargs['y1'] / image_height

        return kwargs
