from wai.common.geometry import Polygon, Rectangle, Point


def polygon_from_rectangle(rectangle: Rectangle) -> Polygon:
    """
    Creates a rectangular polygon from the given rectangle.

    :param rectangle:   The rectangle.
    :return:            The rectangular polygon.
    """
    # Get the rectangle bounds
    left = rectangle.left()
    right = rectangle.right()
    top = rectangle.top()
    bottom = rectangle.bottom()

    # Create a polygon from the bound coordinates
    return Polygon(Point(left, top),
                   Point(right, top),
                   Point(right, bottom),
                   Point(left, bottom))
