# Examples

**Tip:** While building a conversion pipeline command, open a separate terminal to quickly output the available plugins (`wai-annotations plugins`) and the help for a specific plugin (`wai-annotations plugins -o PLUGINNAME`).

**NB:** In the examples below, `input` and `output` represent directories, which you will have to adapt.

## ADAMS to MS-COCO

Also adds additional logging information and removes annotations smaller than 5 pixels in either dimension.

```
wai-annotations convert -v \
    from-adams-od -i input \
    dimension-discarder --min-width 5 --min-height 5 \
    to-coco-od -o output/annotations.json --license-name "my license" --no-images
```

## Monolithic Tensorflow records to sharded ones

Here we are converting a monolithic TFRecords file into a sharded one (`-s 5` - five shards) and only using a subset of labels (`-l label2,label4,label6`):

```
wai-annotations convert \
    from-tfrecords-od -i input/objects.records \
    filter-labels -l label2,label4,label6 \
    to-tfrecords-od -o output/subset.records -s 5 -p labels.pbtxt
```

## ADAMS to Tensorflow records (masks)

The ADAMS input directory contains sub-directories, so we use the `"input/**/*.report"` [glob syntax](https://docs.python.org/3/library/glob.html) to find all `.report` files recursively. The data gets split into train/test with a 80/20 ratio. Supplying split names will automatically insert these names into the output file, i.e., `output/data.tfrecords` will get turned into `output/train/data.tfrecords` and `output/test/data.tfrecords`. No path gets supplied to the file containing the labels (`labels.txt`), it will get placed into the correct output directory automatically:

```
wai-annotations convert \
    from-adams-od -i "input/**/*.report" \
    coerce-mask \
    to-tf-od -o output/data.tfrecords -p labels.txt --split-names train test --split-ratios 80 20
```

## ADAMS invidual layer image segmentation to blue channel JPGs

ADAMS supports the *individual layers* format for image segmentation format, where for each JPG image a PNG with the same file name plus the label suffix is present (e.g.g: 1.jpg -> 1-car.png and 1-person.png). In this case, we only want to include the `car` annotations in the output. The output gets split into train/val with a ratio of 80/20:

```
wai-annotations convert \
    from-blue-channel-is -i "input/**/*.png" --labels car \
    to-blue-channel-is -o output --split-names train val --split-ratios 80 20
```
