"""
Module containing the main entry point functions for converting annotations.
"""
import traceback
from typing import List, Optional

from ._components import components
from ._parser import parser
from ._coercions import coerce_bbox, coerce_mask


def main(args: Optional[List[str]] = None):
    """
    Main function of the annotations converter.

    :param args:    The CLI arguments to the program.
    """
    # Parse the arguments
    namespace = parser.parse_args(args)

    # Instantiate the components from the provided arguments
    reader = components[namespace.input_type][0].instance_from_namespace(namespace)
    input_converter = components[namespace.input_type][1].instance_from_namespace(namespace)
    output_converter = components[namespace.output_type][2].instance_from_namespace(namespace)
    writer = components[namespace.output_type][3].instance_from_namespace(namespace)

    # Create the input chain
    input_chain = input_converter.convert_all(reader.load())

    # Add a coercion if specified
    if namespace.coerce == "bbox":
        input_chain = map(coerce_bbox, input_chain)
    elif namespace.coerce == "mask":
        input_chain = map(coerce_mask, input_chain)

    # Finish the chain with the output components
    writer.save(output_converter.convert_all(input_chain))


def sys_main() -> int:
    """
    Runs the main function using the system cli arguments, and
    returns a system error code.

    :return:    0 for success, 1 for failure.
    """
    try:
        main()
        return 0
    except Exception:
        print(traceback.format_exc())
        return 1
