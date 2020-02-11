from typing import Dict, List, Optional, Set

from ..core.logging import LoggingEnabled


class ROIObject(LoggingEnabled):
    """
    Holds a detected object from a ROI file.
    """
    # The ordered required arguments to ROIObject
    required_keywords = ("x0", "y0", "x1", "y1",
                         "x0n", "y0n", "x1n", "y1n",
                         "label", "label_str", "score")

    # The ordered optional arguments to ROIObject
    optional_keywords = ("poly_x", "poly_y", "poly_xn", "poly_yn",
                         "minrect_w", "minrect_h")

    # The ordered keyword arguments to ROIObject
    keywords = required_keywords + optional_keywords

    # Cached set representations of keywords for fast lookups
    required_keyword_set: Set[str] = set(required_keywords)
    optional_keyword_set: Set[str] = set(optional_keywords)
    keyword_set: Set[str] = set(keywords)

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

    def image_width(self) -> int:
        """
        Calculates the source image's width.

        :return:    The source image's width.
        """
        if self.x0n != 0.0:
            return round(self.x0 / self.x0n)
        else:
            return round(self.x1 / self.x1n)

    def image_height(self) -> int:
        """
        Calculates the source image's height.

        :return:    The source image's height.
        """
        if self.y0n != 0.0:
            return round(self.y0 / self.y0n)
        else:
            return round(self.y1 / self.y1n)

    def as_dict(self) -> Dict[str, str]:
        """
        Gets a dictionary representation of this object.

        :return:    A dict.
        """
        # Create a result dict
        result = {}

        # Process each keyword in turn
        for keyword in self.keywords:
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

        return ROIObject(**kwargs)

    @classmethod
    def _parse(cls, keyword: str, value: str):
        """
        Parses the string representation of a value to its internal type.

        :param keyword: The name of the attribute.
        :param value:   The string representation of the attribute's value.
        """
        # Float types
        if keyword in {"x0", "y0", "x1", "y1", "x0n", "y0n", "x1n", "y1n", "score",
                       "minrect_w", "minrect_h"}:
            return float(value) if value is not "" else None

        # Int types
        if keyword in {"label"}:
            return int(value)

        # List of float types
        if keyword in {"poly_x", "poly_y", "poly_xn", "poly_yn"}:
            return list(map(float, value.split(","))) if value is not "" else None

        # All other attributes are strings
        return value
