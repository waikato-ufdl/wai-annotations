"""
Makes sure tensorflow is available. To utilise, just import this module.
"""
try:
    import tensorflow
except ImportError as e:
    raise RuntimeError("No tensorflow library found\n"
                       "Please install either tensorflow or tensorflow-gpu\n"
                       "    pip install tensorflow\n"
                       "    pip install tensorflow-gpu") from e

# Ensure we're in eager execution mode
from .compat import ensure_eager_execution
ensure_eager_execution()
