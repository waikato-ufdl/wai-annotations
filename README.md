# wai-annotations
Python library for converting image and object annotations formats into each other.

## Installation

You can use pip to install the library:

```
pip install wai.annotations
```

## Supported Formats

Conversions to/from the following annotation formats are currently implemented. The
short-form is the keyword to specify to the command-line arguments.

* `adams`:      [ADAMS reports](https://adams.cms.waikato.ac.nz/)
* `coco`:       [MS-COCO](http://cocodataset.org/)
* `vgg`:        [VGG](https://www.robots.ox.ac.uk/~vgg/)
* `tfrecords`:  [Tensorflow TFRecords](https://www.tensorflow.org/tutorials/load_data/tfrecord)
* `roi`:        [ROI CSV]()

## Usage

```
convert-annotations [GLOBAL OPTIONS] input-type [INPUT OPTIONS] output-type [OUTPUT OPTIONS]
```

The input-type and output-type should be keywords from the **Supported Formats** section above.
Global options are options that are format-agnostic. Each format also has its own format-specific
options, which depend on whether it is the input or output of the conversion.

### Global Options

* `-v`, `--verbosity`: Optional argument to set the logging verbosity of the conversion. Can be
                       specified multiple times to further increase verbosity.

* `-f`, `--force`: Optional argument to coerce the annotation boundaries into a specific type.
                   Set to `bbox` to coerce polygon mask boundaries into a bounding box that
                   tightly contains all polygon points. Set to `mask` to convert bounding box
                   boundaries into polygon masks by creating a box-shaped polygon matching the
                   original.

* `-e`, `--extensions`: Optional argument to specify the order of preference for image types
                        when searching for images related to annotations files. Should be a
                        comma-separated list of extensions. Defaults to `png,jpg` if not specified.
                    
### Input Options

* `-i`, `--inputs`: Optional argument specifying the input files to convert. Can be specified
                    multiple times to build up the set of input files. Uses glob syntax to match
                    multiple files at once. Formats: all.
                   
* `-n`, `--negatives`: Optional argument specifying images to include in the converted data-set as
                       negative examples (contains no annotations). Can be specified multiple times
                       and uses glob syntax, same as `--inputs`. Formats: all.
                       
* `-I`, `--input-files`: Optional argument specifying the input files to convert. Unlike `-inputs`,
                         each matched file is read from disk as a text file containing a list of input
                         files to convert. Can be specified multiple times to build up the set of input
                         files. Uses glob syntax to match multiple files at once. Formats: all.
                         
* `-N`, `--negative-files`: Optional argument specifying images to include in the converted data-set as
                            negative examples (contains no annotations). Unlike `-negatives`, each matched
                            file is read from disk as a text file containing a list of negative files to
                            convert. Can be specified multiple times and uses glob syntax, same as
                            `--inputs`. Formats: all.

* `-m`, `--mapping`: Optional argument specifying a mapping from one label to another. Specify as
                     `old=new`, where `old` is the current label in the input files and `new` is the
                     label it should be mapped to in the output files. Can be specified multiple times
                     to map several labels at once, including mapping multiple `old` labels to the same
                     `new` label. It is an error to specify multiple `new` labels for the same `old`
                     label. Formats: all.
                     
* `-p`, `--prefixes`: Optional comma-separated list of object prefixes to look for in ADAMS report files.
                      If not specified, all object prefixes are converted. Formats: `adams`.
                      
* `--prefix`, `--suffix`: Optional prefix/suffix to consider when reading ROI annotation files. Defaults
                          to the empty string and `-rois.csv` respectively. Only useful for finding the
                          image associated to an empty annotations file. See the options of the same
                          names under Output Options for an example of how this works, but here it is
                          applied in reverse to get the original image name. Formats: `roi`.

### Output Options

* `-o`, `--output`: Required argument specifying the output file or directory to save the converted
                    annotations into. Formats: all.
                    
* `-l`, `--labels`: Optional comma-separated list specifying the labels to include in the output format.
                    If omitted, all labels are included, subject to parsing the `--regexp` option. Labels
                    tested are those after the mapping stage specified by `--mapping`. Formats: all.
                    
* `-r`, `--regexp`: Optional argument specifying a regular expression to use to match labels that should
                    be included in the output format. If omitted, all labels are included, subject to
                    parsing the `--labels` option. Labels tested are those after the mapping stage
                    specified by `--mapping`. Formats: all.
                    
**N.B.**: If both the `--labels` and `--regexp` options are specified, labels that match either condition
          will be output.
          
* `--no-images`: Optional flag to only write the annotations file out to disk. If omitted, the input images
                 are also written to the output directory. Formats: all except `tfrecords`.
                 
* `--license-name`: Optional argument specifying the name of the license to associate with the images. If
                    omitted, defaults to `"default"`. Formats: `coco`.
                    
* `--license-url`: Optional argument specifying the URL for the image license. If omitted, defaults to the
                   empty string. Formats: `coco`.
                   
* `-s`, `--shards`: Optional argument specifying the number of sharded output files to write TFRecords into.
                    If omitted, defaults to unsharded output (a single record file). Formats: `tfrecords`.
                    
* `-p`, `--protobuf`: Optional argument specifying the name of a file to write the label mapping into, in
                      protobuf format. If omitted, no such file is written. Formats: `tfrecords`.
                      
* `-d`, `--image-dimensions`: Optional argument specifying the width and height to use for images that can't
                              infer this information from the input data. Formats: `roi`.
                      
* `--prefix`, `--suffix`: Optional prefix/suffix to attach to the filename used when writing ROI annotation
                          files. Defaults to the empty string and `-rois.csv` respectively. For example, if
                          the image filename was `my-image.png`, and the options `--prefix=annotations-for-`
                          and `--suffix=-in-roi-format.csv` were supplied, the annotations file would be
                          `annotations-for-my-image-in-roi-format.csv`. Formats: `roi`.

## Examples

Create a MS-COCO annotations file for a directory of images and ADAMS report annotations:

```
    convert-annotations \
        adams -i /path/to/reports \
        coco -o /path/to/images/coco-annotations.json --license-name "my license" --no-images
```

Create sharded Tensorflow records with a subset of the labelled objects from a monolithic original:

```
    convert-annotations \
        tfrecords -i /path/to/objects.records \
        tfrecords -o /path/to/subset.records -l label2,label4,label6 -s 5 -p label_map.proto
```
