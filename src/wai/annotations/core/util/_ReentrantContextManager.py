from typing import Generic, TypeVar, ContextManager
from weakref import finalize

# The type of the managed context-manager
CMType = TypeVar("CMType", bound=ContextManager)


class ReentrantContextManager(Generic[CMType]):
    """
    A context-manager that manages another context-manager, allowing it
    to be kept open without exiting/re-entering the context.
    """
    def __init__(self, managed: CMType):
        # The managed context-manager
        self._managed: CMType = managed

        # The result of calling the __enter__ method
        self._enter_result = None

        # Whether the __enter__ method has been called
        self._entered: bool = False

        # A finaliser which closes the context-manager if we are
        # garbage-collected before doing so ourselves
        self._finaliser = None

    def __enter__(self):
        # Enter the context if we haven't already
        if not self._entered:
            self._enter_result = self._managed.__enter__()
            self._entered = True
            self._finaliser = finalize(self, self.finish, None, None, None)

        return self._enter_result

    def __exit__(self, exc_type, exc_val, exc_tb):
        # Only exit the context if completion was abnormal. Otherwise keep
        # the context open
        if exc_type is not None:
            return self.finish(exc_type, exc_val, exc_tb)

    def finish(self, exc_type=None, exc_val=None, exc_tb=None):
        # Finish is idempotent
        if not self._entered:
            return

        # Exit the context
        exit_result = self._managed.__exit__(exc_type, exc_val, exc_tb)
        self._enter_result = None
        self._entered = False

        # No longer require finalisation
        self._finaliser.detach()
        self._finaliser = None

        return exit_result
