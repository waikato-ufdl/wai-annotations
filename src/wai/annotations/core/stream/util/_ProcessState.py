from ...util import InstanceState, StateType


class ProcessState(InstanceState[StateType]):
    """
    Descriptor for stream processing state that automatically resets
    on each application of a pipeline.
    """
    pass
