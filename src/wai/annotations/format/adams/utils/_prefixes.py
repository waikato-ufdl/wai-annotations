"""
Utility functions for working with object prefixes in ADAMS reports.
"""
from typing import Set, Dict

from wai.common.adams.imaging.locateobjects import LocatedObjects
from wai.common.file.report import Report

from ....domain.image.object_detection.util import get_object_prefix, set_object_prefix


def find_all_prefixes(report: Report) -> Set[str]:
    """
    Finds all prefixes in the given report.

    :param report:  The report.
    :return:        A set of prefixes in the report.
    """
    # Create the empty set to fill
    prefixes: Set[str] = set()

    # Process all fields for prefixes
    for field in report.get_fields():
        # Get the field name
        name = field.name

        # Extract the prefix if it has one
        if "." in name:
            prefixes.add(name[:name.index(".")])

    return prefixes


def divide_by_prefix(located_objects: LocatedObjects) -> Dict[str, LocatedObjects]:
    """
    Divides a single set of located objects into sub-sets where
    each shares a common prefix.

    :param located_objects:     The located objects.
    :return:                    Map from prefix to located objects with that prefix.
    """
    # Create the empty map
    prefix_objects: Dict[str, LocatedObjects] = {}

    # Process each object into the map
    for located_object in located_objects:
        # Get the object's prefix
        prefix: str = get_object_prefix(located_object)

        # Create a new group for the prefix the first time we encounter it
        if prefix not in prefix_objects:
            prefix_objects[prefix] = LocatedObjects()

        # Add the object to its prefix group
        prefix_objects[prefix].append(located_object)

    return prefix_objects


def remove_prefix_metadata(located_objects: LocatedObjects):
    """
    Removes the prefix meta-data from the located objects.

    :param located_objects:     The located objects.
    """
    for located_object in located_objects:
        set_object_prefix(located_object, None)
