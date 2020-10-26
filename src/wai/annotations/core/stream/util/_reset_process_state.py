from ._ProcessState import ProcessState


def reset_process_state(stream_element):
    """
    Reset all process-state for a given stream element.

    :param stream_element:  The stream element to reset.
    """
    # Get the class of the element
    element_type = type(stream_element)

    # Look for all ProcessState descriptors
    for attr_name in dir(element_type):
        # Get the attribute of the class
        attr = getattr(element_type, attr_name)

        # If it's a ProcessState descriptor, delete it from the instance
        if attr is ProcessState:
            delattr(stream_element, attr_name)


def reset_all_process_state(*stream_elements):
    """
    Resets the process-state for all given stream elements.

    :param stream_elements:     The stream elements to reset.
    """
    for stream_element in stream_elements:
        reset_process_state(stream_element)
