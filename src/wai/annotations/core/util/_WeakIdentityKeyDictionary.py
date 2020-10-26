from typing import TypeVar, MutableMapping, Iterator, Generic
from weakref import WeakValueDictionary, WeakKeyDictionary

KeyType = TypeVar("KeyType")
ValueType = TypeVar("ValueType")


class ID(Generic[KeyType]):
    """
    Helper class for the WeakIdentityKeyDictionary class, which references
    the ID of an object.
    """
    def __init__(self, key: KeyType):
        self._identity: int = id(key)

    def __hash__(self):
        return self._identity

    def __eq__(self, other):
        if isinstance(other, ID):
            other = other._identity
        return isinstance(other, int) and other == self._identity


class WeakIdentityKeyDictionary(MutableMapping[KeyType, ValueType]):
    """
    Dictionary which weakly references keys by their identity.
    """
    def __init__(self):
        self._keys: MutableMapping[ID, KeyType] = WeakValueDictionary()
        self._values: MutableMapping[ID, ValueType] = WeakKeyDictionary()

    def __setitem__(self, k: KeyType, v: ValueType):
        identity = ID(k)
        self._keys[identity] = k
        self._values[identity] = v
        
    def __delitem__(self, v: KeyType):
        identity = ID(v)
        del self._keys[identity]
        del self._values[identity]

    def __getitem__(self, k: KeyType) -> ValueType:
        identity = ID(k)
        return self._values[identity]

    def __len__(self) -> int:
        return len(self._values)

    def __iter__(self) -> Iterator[KeyType]:
        return iter(self._keys.values())

    def __contains__(self, item: KeyType) -> bool:
        return id(item) in self._keys
