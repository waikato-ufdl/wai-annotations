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
                        
* `--min-width`: Optional integer to discard annotations with width less than this value.

* `--max-width`: Optional integer to discard annotations with width greater than this value.

* `--min-height`: Optional integer to discard annotations with height less than this value.

* `--max-height`: Optional integer to discard annotations with height greater than this value.

* `--min-area`: Optional integer to discard annotations with area less than this value.

* `--max-area`: Optional integer to discard annotations with area greater than this value.

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
                     
* `-p`, `--prefixes`: Optional list of object prefixes to look for in ADAMS report files.
                      If not specified, all object prefixes are converted. Formats: `adams`.
                      
* `--prefix`, `--suffix`: Optional prefix/suffix to consider when reading ROI annotation files. Defaults
                          to the empty string and `-rois.csv` respectively. Only useful for finding the
                          image associated to an empty annotations file. See the options of the same
                          names under Output Options for an example of how this works, but here it is
                          applied in reverse to get the original image name. Formats: `roi`.
                          
* `--sample-stride`: Optional integer which uses a lower-resolution view of the mask to generate
                     a polygon for the annotation. E.g. a value of 2 would look at every second
                     pixel in the mask (in both x- and y-directions). This in theory results in
                     a more-coarsely-grained polygon but at the benefit of taking less time to
                     compute. Formats: `tfrecords`.

* `--mask-threshold`: Optional value between 0.0 and 1.0 which determines the mask values that are
                      considered inside the polygon when generating a polygon from the mask.
                      Formats: `tfrecords`.
                      
* `--seed`: Optional value to randomise the order in which files are loaded. Useful in conjunction
            with the split- options to create randomised sub-sets. Formats: all.
            N.b. The seed is supplied to a pseudo-random number generator, so using the same seed
            multiple times on the same set of input files will result in the same read order.

### Output Options

* `-o`, `--output`: Required argument specifying the output file or directory to save the converted
                    annotations into. Formats: all.
                    
* `-l`, `--labels`: Optional list specifying the labels to include in the output format. If omitted, all
                    labels are included, subject to parsing the `--regexp` option. Labels tested are those
                    after the mapping stage specified by `--mapping`. Formats: all.
                    
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
                          
* `--pretty`: Optional flag for JSON-based formats which tells them to output their JSON files with pretty indentation.
              If not included, JSON files are saved in compact-form instead. Formats: `coco`, `vgg`.

* `--comments`: Optional flag to specify comments to write to the beginning of the annotations files.
                Formats: `roi`.
                
* `--size-mode`: Optional flag to write ROI files with x, y, w, h-style headers rather than the standard
                 x0, y0, x1, y1-style headers. Formats: `roi`.

* `--split-names`, `--split-ratios`: Allows the files to be split into subsets. `--split-names` should be a list
                                     of names for the splits, and `--split-ratios` should be a list of the
                                     proportions of the files that should go into each split. Each split is put
                                     into a sub-directory with the split name for that split. Formats: all.
                                     E.g. `--split-names train test --split-ratios 7 3` would create two subsets,
                                     train and test, with 70% of the images going into train and 30% going into
                                     test.
                                     N.b. If the number of split names given is different to the number of ratios
                                     given, the shorter of the two lists will be used, and the additional values in
                                     the longer list will be ignored.

## Plugins

The **wai.annotations** library supports a plug-in mechanism for adding your own conversion formats.
To create a plugin format, you need to create a package which provides implementations of some abstract types
from the `wai.annotations.core` package. The process is detailed below.

### 1. Create a Representation of the External Format

An external format is a representation of a single image and the annotations that are identified on that image. There
is no abstract base class for this, the representation can be whatever you like. However the information the format
should contain is:

* The file-name of the image, with extension and no directory elements.
* The image's binary data (technically optional but some conversions will fail without it).
* A collection of annotations for the image, each containing:
  * The co-ordinates of the top-left corner of the annotation's bounding-box.
  * The width and height of the bounding-box.
  * The label for the annotation.
  * (Optionally) data for a detailed bounds of the annotation (e.g. a polygon).
  * (Optionally) a super-category for the annotation.

### 2a. Create a Reader and ExternalFormatConverter (if the format is required for input)

Using a format as input requires two components: a `Reader` to read instances of the external format from disk; and an
`ExternalFormatConverter` to convert those instances into the `wai.annotations` internal format.

To create a reader for your format, inherit from the abstract base class `wai.annotations.core.components.Reader`. Two
methods require implementation: `read_annotation_file`, which takes a filename as a string (including path elements) and
should return an iterator of instances of your external format as read from that file (if each file contains only one
instance, i.e. only annotations for one image, just **yield** the single instance); and `image_info_to_external_format`,
which takes an image file (described by a `wai.annotations.core.ImageInfo` object) and returns an instance of your
external format with no annotations (this is for using images as negative-only examples).

**Example Reader**
```python
from typing import Iterator

from wai.annotations.core import ImageInfo
from wai.annotations.core.components import Reader

# Your definition of the external format (probably defined elsewhere...)
MyExternalFormat: type = ...

class MyReader(Reader[MyExternalFormat]):
    def read_annotation_file(self, filename: str) -> Iterator[MyExternalFormat]:
        # Open the file
        with open(filename, "rb") as file:
            # Yield the single instance from the file
            yield MyExternalFormat.from_binary_file_contents(file.read())
    
    def image_info_to_external_format(self, image_info: ImageInfo) -> MyExternalFormat:
        return MyExternalFormat.from_image(image_info.filename, image_info.data)
```

To create an external-format converter, inherit from the abstract base class
`wai.annotations.core.components.ExternalFormatConverter`. Only one method requires implementation: `_convert`, which
takes an instance of your external format and produces an instance of the wai.annotations internal format (imported 
from `wai.annotations.core`).

**Example ExternalFormatConverter**
```python
from wai.annotations.core import InternalFormat
from wai.annotations.core.components import ExternalFormatConverter

# Your definition of the external format (probably defined elsewhere...)
MyExternalFormat: type = ...

class MyExternalFormatConverter(ExternalFormatConverter[MyExternalFormat]):
    def _convert(self, instance: MyExternalFormat) -> InternalFormat:
        return InternalFormat(instance.get_image_info(),
                              instance.get_located_objects())
```

### 2b. Create an InternalFormatConverter and Writer (if the format is required for output)

For outputting annotations in your external format, you need a `InternalFormatConverter` to convert the internal format
instances to your external format, and a `Writer` to write the instances to disk.

To create the internal-format converter, inherit from the `wai.annotations.core.components.InternalFormatConverter`
abstract base class. Then implement the `convert_unpacked` method, which takes an unpacked instance in the internal
format (a `wai.annotations.core.ImageInfo` object and a `wai.common.adams.imaging.locateobjects.LocatedObjects` object)
and returns an instance of your external format.

**Example InternalFormatConverter**
```python
from wai.annotations.core import ImageInfo
from wai.annotations.core.components import InternalFormatConverter
from wai.annotations.core.utils import get_object_label
from wai.common.adams.imaging.locateobjects import LocatedObjects

# Your definition of the external format (probably defined elsewhere...)
MyExternalFormat: type = ...

class MyInternalFormatConverter(InternalFormatConverter[MyExternalFormat]):
    def convert_unpacked(self,
                         image_info: ImageInfo,
                         located_objects: LocatedObjects) -> MyExternalFormat:
        # Create an empty instance
        instance =  MyExternalFormat.from_image(image_info.filename, image_info.data)
        
        # Add the annotations
        for located_object in located_objects:
            instance.add_annotation(located_object.x,
                                    located_object.y,
                                    located_object.width,
                                    located_object.height,
                                    get_object_label(located_object))
                                    
        return instance
```

To create the writer, inherit from the `wai.annotations.core.components.Writer` abstract base class. Then implement the
`expects_file`, `output_help_text`, `write`  and `extract_image_info_from_external_format` methods.

`expects_file` and `output_help_text` are both part of the same mechanism, determining whether the writer writes a
single annotations file for all images, or a separate file for each image. `expects_file` should return a boolean `True`
if the `output` option should be the name of a file to write to, or `False` if it should be a directory to write files
into. `output_help_text` should return a help-string indicating which should be provided.

`write` receives a series of instances in your external format, as well as the file/directory to write to (as above). It
should write the instances to that file/directory on disk.

`extract_image_info_from_external_format` takes an instance of your external format and should return an instance of
`wai.annotations.core.ImageInfo` containing the information about the image stored in the instance. If your external
format uses `ImageInfo` to contain its image data already, this method can simply return that object. Otherwise it
must be extracted and returned in a new `ImageInfo` object.

**Example Writer**
```python
import os
from typing import Iterable
from wai.annotations.core import ImageInfo
from wai.annotations.core.components import Writer

# Your definition of the external format (probably defined elsewhere...)
MyExternalFormat: type = ...

class MyWriter(Writer[MyExternalFormat]):
    def expects_file(self) -> bool:
        # Our format writes annotations for each image to its own file,
        # so we expect a directory to write those files into
        return False
    
    @classmethod    
    def output_help_text(cls) -> str:
        # Our format uses the '.mef' extension
        return "the directory to write the .mef files into"
        
    def write(self, instances: Iterable[MyExternalFormat], path: str):
        for instance in instances:
            # The filename is the image filename with a .mef extension
            filename = os.path.splitext(instance.image_filename)[0] + ".mef"
            
            # Open and write the file
            with open(os.path.join(path, filename), "wb") as file:
                instance.write_to_file(file)

    def extract_image_info_from_external_format(self, instance: MyExternalFormat) -> ImageInfo:
        return ImageInfo(instance.image_filename, instance.image_data)
```

Two abstract sub-types of `Writer` exist to support some common format conventions.

Firstly, `wai.annotations.core.components.SeparateImageWriter` is a sub-class of `Writer` for formats that don't store
the image data in the same file as the annotations, instead storing them as plain images on disk. Instead of
implementing `write`, implement `write_without_images`, which takes the same input parameters, but only needs to write
the annotations file/files to disk. Writing of the image files is handled automatically.

Secondly, `wai.annotations.core.components.JSONWriter` extends `SeparateImageWriter` for formats that write a single
JSON file containing their annotations. It provides an implemented `expects_file` (however `output_help_text` still
needs implementing), and `write_without_images` is also implemented. Instead, inheritors of this base class should
implement `create_json_object`, which takes the stream of instances in your external format and creates an instance of
 `wai.json.object.JSONObject` to be serialised to disk.

### 3. Create a Format Specifier to Expose your Components

Now that we have some conversion components specified, we can specify the format as a whole. This is done by inheriting
from `wai.annotations.core.FormatSpecifier`, and filling in the initialiser fields with our newly-defined classes. All
fields are optional, but a `Reader` and `ExternalFormatConverter` are required for the format to be available for input,
and a `Writer` and `InternalFormatConverter` are required for the format to be available for output.

**Example FormatSpecifier**
```python
from wai.annotations.core import FormatSpecifier
from wai.annotations.core.components import Reader, ExternalFormatConverter, InternalFormatConverter, Writer

# Your definition of the external format (probably defined elsewhere...)
MyExternalFormat: type = ...

# Your component definitions (probably defined elsewhere...)
class MyReader(Reader[MyExternalFormat]): pass
class MyExternalFormatConverter(ExternalFormatConverter[MyExternalFormat]): pass
class MyInternalFormatConverter(InternalFormatConverter[MyExternalFormat]): pass
class MyWriter(Writer[MyExternalFormat]): pass

class MyFormatSpecifier(FormatSpecifier):
    def __init__(self):
        super().__init__(MyReader, MyExternalFormatConverter, MyInternalFormatConverter, MyWriter)
```

### 4. Add the Format Specifier to the Entry Points Group

For `wai.annotations` to find your format, it must be added to the `wai.annotations.formats` entry-point group. Do this
by adding an entry for the format in your `setup.py` script, using a short name for your format as the key.

**Example setup.py**
```python
from setuptools import setup

setup(
    entry_points={
        # Our format will be identified as 'mef', and the specifier class
        # is located in the 'mef.spec' package.
        "wai.annotations.formats": ["mef=mef.spec:MyFormatSpecifier"]
    }
)
```

That's it! When installed along-side `wai.annotations`, your format will be discovered and become usable as an
input/output format (depending on the components specified).

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
