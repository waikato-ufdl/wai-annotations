from ....domain.image import ImageInfo
from .._ensure_available import tensorflow as tf
from ._make_feature import make_feature


def negative_example(image_info: ImageInfo):
    """
    Creates an empty example (for images with no annotations).

    :return:    The empty example.
    """
    return tf.train.Example(
        features=tf.train.Features(
            feature={
                'image/height': make_feature(image_info.height),
                'image/width': make_feature(image_info.width),
                'image/filename': make_feature(image_info.filename),
                'image/source_id': make_feature(image_info.filename),
                'image/encoded': make_feature(image_info.data),
                'image/format': make_feature(image_info.format.get_default_extension()),
                'image/object/bbox/xmin': tf.train.Feature(float_list=tf.train.FloatList(value=[])),
                'image/object/bbox/xmax': tf.train.Feature(float_list=tf.train.FloatList(value=[])),
                'image/object/bbox/ymin': tf.train.Feature(float_list=tf.train.FloatList(value=[])),
                'image/object/bbox/ymax': tf.train.Feature(float_list=tf.train.FloatList(value=[])),
                'image/object/class/text': tf.train.Feature(bytes_list=tf.train.BytesList(value=[])),
                'image/object/class/label': tf.train.Feature(int64_list=tf.train.Int64List(value=[])),
                'image/object/mask': tf.train.Feature(bytes_list=tf.train.BytesList(value=[]))
            }
        )
    )
