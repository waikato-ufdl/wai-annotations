"""
Utilities for working with streams/pipelines.
"""
from ._enforce_calling_semantics import enforce_calling_semantics
from ._FunctionStreamSink import FunctionStreamSink
from ._IterableStreamSource import IterableStreamSource
from ._ProcessState import ProcessState
from ._RequiresNoFinalisation import RequiresNoFinalisation
from ._reset_process_state import reset_process_state, reset_all_process_state
