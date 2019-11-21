def format_sharded_filename(base_name: str, shards: int, index: int):
    """
    Formats the filename for a shard in sharded output.

    :param base_name:   The base filename to use.
    :param shards:      The number of shards being output, total.
    :param index:       The index of the current shard [0:shards).
    :return:            The formatted filename.
    """
    return f"{base_name}-{index:05}-of-{shards:05}"
