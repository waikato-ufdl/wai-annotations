"""
Compatibility layer for working with Tensorflow v1 and v2.
"""
# Get the version of Tensorflow
try:
    import tensorflow
    VERSION = tensorflow.version.VERSION
except Exception as e:
    raise RuntimeError(f"Failed to determine Tensorflow version") from e

# Cast the major version number to an int
try:
    version = int(VERSION[0])
except Exception as e:
    raise RuntimeError(f"Could not parse Tensorflow major version number from '{VERSION}'") from e

# Import the correct compatibility package
if version == 1:
    from .v1 import *
elif version == 2:
    from .v2 import *
else:
    raise RuntimeError(f"Major version number parsed from Tensorflow version ('{VERSION}') "
                       f"was {version}, but should be 1 or 2")
