from ._ProcessState import ProcessState


def reset_process_state(stream_element):
    """
    Reset all process-state for a given stream element.

    :param stream_element:  The stream element to reset.
    """
    # Get the class of the element
    element_type = type(stream_element)

    # Look for all ProcessState descriptors, and delete them to reset them
    for attr_name in dir(element_type):
        if hasattr(element_type, attr_name) and getattr(element_type, attr_name) is ProcessState:
            delattr(stream_element, attr_name)


def reset_all_process_state(*stream_elements):
    """
    Resets the process-state for all given stream elements.

    :param stream_elements:     The stream elements to reset.
    """
    for stream_element in stream_elements:
        reset_process_state(stream_element)
