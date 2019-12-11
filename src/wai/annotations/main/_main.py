"""
Module containing the main entry point functions for converting annotations.
"""
import traceback
from typing import List, Optional

# Make sure a tensorflow library is installed
try:
    import tensorflow
except ImportError as e:
    raise RuntimeError("No tensorflow library found\n"
                       "Please install either tensorflow or tensorflow-gpu\n"
                       "    pip install tensorflow\n"
                       "    pip install tensorflow-gpu")

from ._components import get_reader_class, get_external_format_converter_class, get_internal_format_converter_class, \
    get_writer_class
from ._parser import parser
from ._coercions import coerce_bbox, coerce_mask


def main(args: Optional[List[str]] = None):
    """
    Main function of the annotations converter.

    :param args:    The CLI arguments to the program.
    """
    # Parse the arguments
    namespace = parser.parse_args(args)

    # Make sure an input and output format were specified
    # (currently no required flag for sub-parsers)
    if not hasattr(namespace, "input_type"):
        parser.error(f"No input type provided")
    elif not hasattr(namespace, "output_type"):
        parser.error(f"No output type provided")

    # Get the input and output formats
    input_format = namespace.input_type
    output_format = namespace.output_type

    # Instantiate the components from the provided arguments
    reader = get_reader_class(input_format).instance_from_namespace(namespace)
    input_converter = get_external_format_converter_class(input_format).instance_from_namespace(namespace)
    output_converter = get_internal_format_converter_class(output_format).instance_from_namespace(namespace)
    writer = get_writer_class(output_format).instance_from_namespace(namespace)

    # Create the input chain
    input_chain = input_converter.convert_all(reader.load())

    # Add a coercion if specified
    if namespace.force == "bbox":
        input_chain = map(coerce_bbox, input_chain)
    elif namespace.force == "mask":
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
