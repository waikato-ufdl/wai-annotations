def ensure_eager_execution():
    """
    Ensures that Tensorflow is in eager-execution mode.
    """
    # Tensorflow V2 is eager by default
    from tensorflow import executing_eagerly
    if not executing_eagerly():
        raise RuntimeError(f"Tensorflow V2 not in eager-execution mode")
