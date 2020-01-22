import os


def roi_filename_for_image(image_filename: str) -> str:
    """
    Creates a filename for the ROI CSV file from the given image filename.

    :param image_filename:  The image filename.
    :return:                The ROI CSV filename.
    """
    return f"{os.path.splitext(image_filename)[0]}-roi.csv"
