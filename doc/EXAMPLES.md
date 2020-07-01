# Examples

## Create a MS-COCO annotations file for a directory of images and ADAMS report annotations:

Also adds additional logging information and removes annotations smaller than 5 pixels in
either dimension.

```
    convert-annotations -v \
        from-adams -i /path/to/reports \
        dimension-discarder --min-width 5 --min-height 5
        to-coco -o /path/to/images/coco-annotations.json --license-name "my license" --no-images
```

## Create sharded Tensorflow records with a subset of the labelled objects from a monolithic original:

```
    convert-annotations \
        from-tfrecords -i /path/to/objects.records \
        to-tfrecords -o /path/to/subset.records -l label2,label4,label6 -s 5 -p label_map.proto
```
