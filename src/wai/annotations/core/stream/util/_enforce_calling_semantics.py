from functools import wraps
from typing import Tuple, Callable

from ..error import DoneNeverCalled, ThenCalledAfterDone
from .._typing import ThenFunction, DoneFunction


def enforce_calling_semantics(
        *funcs: Callable,
        then: ThenFunction,
        done: DoneFunction
) -> Tuple[Callable, ...]:
    """
    Creates modified versions of the given functions that binds the given
    'then' and 'done' functions to their arguments, and ensures that they
    are called with the correct semantics from within them.

    :param funcs:   The functions that will be calling the 'then' and 'done' functions.
    :param then:    The 'then' function.
    :param done:    The 'done' function.
    :return:        The bound functions with calling semantics enforced.
    """
    # Make sure at least one function was provided
    if len(funcs) == 0:
        raise Exception("No funcs provided")

    # Create a closure to track if 'done' has been called
    done_called: bool = False

    # Define a 'then' function which makes sure 'done' hasn't been called
    @wraps(then)
    def enforced_then(element):
        # If 'done' has been called already, error
        if done_called:
            raise ThenCalledAfterDone()

        # Call 'then'
        then(element)

    # Define a 'done' function which is idempotent
    @wraps(done)
    def enforced_done():
        # We're assigning to the closure, so need to specify the non-local identifier
        nonlocal done_called

        # If 'done' was already called, short-circuit
        if done_called:
            return

        # Call the actual 'done' function
        done()

        # 'done' has now been called
        done_called = True

    # Create a list of the enforced versions of the supplied functions
    bound_funcs = [
        bind_funcs(func, enforced_then, enforced_done)
        for func in funcs
    ]

    # Create a special enforced function for the last function, which
    # also requires that 'done' have been called by the time it returns
    last_bound_func = bound_funcs[-1]
    @wraps(last_bound_func)
    def enforced_func(*args, **kwargs):
        # Call the function
        result = last_bound_func(*args, **kwargs)

        # If it completes successfully without calling 'done', raise an error
        if not done_called:
            raise DoneNeverCalled()

        return result

    # Replace the last function with the special case version
    bound_funcs[-1] = enforced_func

    return tuple(bound_funcs)


def bind_funcs(func, then, done):
    """
    Binds the 'then' and 'done' functions to the arguments of the given
    function.

    :param func:    The function to bind the 'then' and 'done' functions to.
    :param then:    The 'then' function.
    :param done:    The 'done' function.
    :return:        The bound function.
    """
    @wraps(func)
    def enforced_func(*args, **kwargs):
        # Add the 'then' and 'done' functions to the call arguments
        kwargs.update(then=then, done=done)

        # Call the function
        return func(*args, **kwargs)

    return enforced_func
