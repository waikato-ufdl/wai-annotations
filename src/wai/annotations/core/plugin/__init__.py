# Check the registry is valid first
from ._check_registry import check_registry
check_registry()
del check_registry

from ._registry import registry
