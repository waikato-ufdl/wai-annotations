def ensure_eager_execution():
    """
    Ensures that Tensorflow is in eager-execution mode.
    """
    from tensorflow.compat.v1 import enable_eager_execution
    enable_eager_execution()
