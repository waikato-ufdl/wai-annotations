class RequiresNoFinalisation:
    """
    Mixin for stream processors/sinks which don't require finalisation.
    """
    def finish(self, *args, **kwargs):
        # Find the 'done' function if one is given
        done = (
            kwargs['done'] if 'done' in kwargs
            else args[1] if len(args) >= 2
            else None)

        # Call the 'done' function (it's idempotent so doesn't matter
        # if it has already been called)
        if done is not None:
            done()
