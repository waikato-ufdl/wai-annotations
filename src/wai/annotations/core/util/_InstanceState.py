from typing import TypeVar, Generic, Callable, Any, Type

from ._WeakIdentityKeyDictionary import WeakIdentityKeyDictionary

StateType = TypeVar("StateType")
OwnerType = TypeVar("OwnerType")


class InstanceState(Generic[StateType]):
    """
    Descriptor for adding state to an object. The state is kept in a dictionary
    in the descriptor, rather than attached to the object itself.
    """
    def __init__(self, initialiser: Callable[[OwnerType], StateType]):
        # The initialiser which provides the state value lazily
        self._initialiser: Callable[[OwnerType], StateType] = initialiser

        # The state for each accessing instance
        self._state: WeakIdentityKeyDictionary[OwnerType, StateType] = WeakIdentityKeyDictionary()

    def __set_name__(self, owner: Type[OwnerType], name: str):
        # Nothing done with at bind-time
        pass

    def __get__(self, instance: OwnerType, owner: Type[OwnerType]) -> StateType:
        # If called on the owner class, return this descriptor
        if instance is None:
            return self

        # If the state has not been initialised, do so now
        if instance not in self._state:
            self._state[instance] = self._initialiser(instance)

        return self._state[instance]

    def __set__(self, instance: OwnerType, value: StateType):
        # Set the value for the state
        self._state[instance] = value

    def __delete__(self, instance: OwnerType):
        del self._state[instance]
