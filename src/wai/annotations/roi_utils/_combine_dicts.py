from typing import Iterable, Dict, Any, List, Set, Tuple


def combine_dicts(dicts: Iterable[Dict[str, Any]]) -> Tuple[List[Dict[str, Any]], Set[str]]:
    """
    Combines a series of ROI-format dictionaries into a list of
    dictionaries with a common set of headers.

    :param dicts:   The dictionaries to combine.
    :return:        The combined dictionaries, and the set of headers for each dictionary.
    """
    # Cache the ROI dicts
    dicts = list(dicts)

    # Combine the headers
    headers = set()
    for roi_dict in dicts:
        headers.update(roi_dict.keys())

    # Add missing headers to each dict
    for roi_dict in dicts:
        for header in headers:
            if header not in roi_dict:
                roi_dict[header] = ""

    return dicts, headers
