"""
Package for utility functions for working with Tensorflow.
"""
from ._extract_feature import extract_feature
from ._make_feature import make_feature
from ._negative_example import negative_example
from ._open_sharded_output_tfrecords import open_sharded_output_tfrecords
from ._ShardCompactor import ShardCompactor
from ._sharded_filenames import format_sharded_filename, sharded_filename_params, is_shard_filename, \
    get_all_sharded_filenames
