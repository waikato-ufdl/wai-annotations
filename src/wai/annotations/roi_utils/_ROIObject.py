from typing import Dict, Tuple


class ROIObject:
    """
    Holds a detected object from a ROI file.
    """
    def __init__(self,
                 x0: float, y0: float, x1: float, y1: float,
                 x0n: float, y0n: float, x1n: float, y1n: float,
                 label: int, label_str: str, score: float):
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

    @classmethod
    def keywords(cls) -> Tuple[str, ...]:
        """
        Gets the names of the keyword parameters to this class.

        :return:    The keyword parameter names.
        """
        return "x0", "y0", "x1", "y1", "x0n", "y0n", "x1n", "y1n", "label", "label_str", "score"

    @classmethod
    def types(cls) -> Tuple[type, ...]:
        """
        Gets the types of the keyword parameters to this class.

        :return:    The keyword parameter types.
        """
        return float, float, float, float, float, float, float, float, int, str, float

    def as_dict(self) -> Dict[str, str]:
        """
        Gets a dictionary representation of this object.

        :return:    A dict.
        """
        return {keyword: str(getattr(self, keyword))
                for keyword in self.keywords()}

    @classmethod
    def from_dict(cls, dict: Dict[str, str]) -> "ROIObject":
        """
        Creates an object instance from the given dictionary.

        :param dict:    The dict.
        :return:        A ROIObject instance.
        """
        return ROIObject(**{keyword: type(dict[keyword])
                            for keyword, type in zip(cls.keywords(), cls.types())})
