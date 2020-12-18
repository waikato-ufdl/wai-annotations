# Plugins
## Source stage
### FROM-ADAMS-IC
Reads image classification annotations in the ADAMS report-format

#### Domain(s):
- **Image Classification Domain**

#### Options:
```
usage: from-adams-ic [-I FILENAME] [-i FILENAME] [-N FILENAME] [-n FILENAME] [--seed SEED] [-e FORMAT FORMAT FORMAT] -c FIELD

optional arguments:
  -I FILENAME, --inputs-file FILENAME
                        Files containing lists of input files (can use glob syntax)
  -i FILENAME, --input FILENAME
                        Input files (can use glob syntax)
  -N FILENAME, --negatives-file FILENAME
                        Files containing lists of negative files (can use glob syntax)
  -n FILENAME, --negative FILENAME
                        Files that have no annotations (can use glob syntax)
  --seed SEED           the seed to use for randomisation
  -e FORMAT FORMAT FORMAT, --extensions FORMAT FORMAT FORMAT
                        image format extensions in order of preference
  -c FIELD, --class-field FIELD
                        the report field containing the image class
```

### FROM-ADAMS-OD
Reads image object-detection annotations in the ADAMS report-format

#### Domain(s):
- **Image Object-Detection Domain**

#### Options:
```
usage: from-adams-od [-I FILENAME] [-i FILENAME] [-N FILENAME] [-n FILENAME] [--seed SEED] [-e FORMAT FORMAT FORMAT] [-p PREFIXES [PREFIXES ...]]

optional arguments:
  -I FILENAME, --inputs-file FILENAME
                        Files containing lists of input files (can use glob syntax)
  -i FILENAME, --input FILENAME
                        Input files (can use glob syntax)
  -N FILENAME, --negatives-file FILENAME
                        Files containing lists of negative files (can use glob syntax)
  -n FILENAME, --negative FILENAME
                        Files that have no annotations (can use glob syntax)
  --seed SEED           the seed to use for randomisation
  -e FORMAT FORMAT FORMAT, --extensions FORMAT FORMAT FORMAT
                        image format extensions in order of preference
  -p PREFIXES [PREFIXES ...], --prefixes PREFIXES [PREFIXES ...]
                        prefixes to parse
```

### FROM-BLUE-CHANNEL-IS
Reads image segmentation files in the blue-channel format

#### Domain(s):
- **Image Segmentation Domain**

#### Options:
```
usage: from-blue-channel-is [-I FILENAME] [-i FILENAME] [-N FILENAME] [-n FILENAME] [--seed SEED] [--image-path-rel PATH] --labels LABEL [LABEL ...]

optional arguments:
  -I FILENAME, --inputs-file FILENAME
                        Files containing lists of input files (can use glob syntax)
  -i FILENAME, --input FILENAME
                        Input files (can use glob syntax)
  -N FILENAME, --negatives-file FILENAME
                        Files containing lists of negative files (can use glob syntax)
  -n FILENAME, --negative FILENAME
                        Files that have no annotations (can use glob syntax)
  --seed SEED           the seed to use for randomisation
  --image-path-rel PATH
                        Relative path to image files from annotations
  --labels LABEL [LABEL ...]
                        specifies the labels for each index
```

### FROM-COCO-OD
Reads image object-detection annotations in the MS-COCO JSON-format

#### Domain(s):
- **Image Object-Detection Domain**

#### Options:
```
usage: from-coco-od [-I FILENAME] [-i FILENAME] [-N FILENAME] [-n FILENAME] [--seed SEED]

optional arguments:
  -I FILENAME, --inputs-file FILENAME
                        Files containing lists of input files (can use glob syntax)
  -i FILENAME, --input FILENAME
                        Input files (can use glob syntax)
  -N FILENAME, --negatives-file FILENAME
                        Files containing lists of negative files (can use glob syntax)
  -n FILENAME, --negative FILENAME
                        Files that have no annotations (can use glob syntax)
  --seed SEED           the seed to use for randomisation
```

### FROM-COMMON-VOICE-SP
Reads speech transcriptions in the Mozilla Common-Voice TSV-format

#### Domain(s):
- **Speech Domain**

#### Options:
```
usage: from-common-voice-sp [-I FILENAME] [-i FILENAME] [-N FILENAME] [-n FILENAME] [--seed SEED] [--rel-path REL_PATH]

optional arguments:
  -I FILENAME, --inputs-file FILENAME
                        Files containing lists of input files (can use glob syntax)
  -i FILENAME, --input FILENAME
                        Input files (can use glob syntax)
  -N FILENAME, --negatives-file FILENAME
                        Files containing lists of negative files (can use glob syntax)
  -n FILENAME, --negative FILENAME
                        Files that have no annotations (can use glob syntax)
  --seed SEED           the seed to use for randomisation
  --rel-path REL_PATH   the relative path from the annotations file to the audio files
```

### FROM-FESTVOX-SP
Reads speech transcriptions in the Festival FestVox format

#### Domain(s):
- **Speech Domain**

#### Options:
```
usage: from-festvox-sp [-I FILENAME] [-i FILENAME] [-N FILENAME] [-n FILENAME] [--seed SEED] [--rel-path REL_PATH]

optional arguments:
  -I FILENAME, --inputs-file FILENAME
                        Files containing lists of input files (can use glob syntax)
  -i FILENAME, --input FILENAME
                        Input files (can use glob syntax)
  -N FILENAME, --negatives-file FILENAME
                        Files containing lists of negative files (can use glob syntax)
  -n FILENAME, --negative FILENAME
                        Files that have no annotations (can use glob syntax)
  --seed SEED           the seed to use for randomisation
  --rel-path REL_PATH   the relative path from the annotations file to the audio files
```

### FROM-INDEXED-PNG-IS
Reads image segmentation files in the indexed-PNG format

#### Domain(s):
- **Image Segmentation Domain**

#### Options:
```
usage: from-indexed-png-is [-I FILENAME] [-i FILENAME] [-N FILENAME] [-n FILENAME] [--seed SEED] [--image-path-rel PATH] --labels LABEL [LABEL ...]

optional arguments:
  -I FILENAME, --inputs-file FILENAME
                        Files containing lists of input files (can use glob syntax)
  -i FILENAME, --input FILENAME
                        Input files (can use glob syntax)
  -N FILENAME, --negatives-file FILENAME
                        Files containing lists of negative files (can use glob syntax)
  -n FILENAME, --negative FILENAME
                        Files that have no annotations (can use glob syntax)
  --seed SEED           the seed to use for randomisation
  --image-path-rel PATH
                        Relative path to image files from annotations
  --labels LABEL [LABEL ...]
                        specifies the labels for each index
```

### FROM-LAYER-SEGMENTS-IS
Reads in the layer-segments image-segmentation format from disk, where each label has a binary PNG storing the mask for that label

#### Domain(s):
- **Image Segmentation Domain**

#### Options:
```
usage: from-layer-segments-is [-I FILENAME] [-i FILENAME] [-N FILENAME] [-n FILENAME] [--seed SEED] [--label-separator SEPARATOR] --labels LABEL [LABEL ...] [--image-path-rel PATH]

optional arguments:
  -I FILENAME, --inputs-file FILENAME
                        Files containing lists of input files (can use glob syntax)
  -i FILENAME, --input FILENAME
                        Input files (can use glob syntax)
  -N FILENAME, --negatives-file FILENAME
                        Files containing lists of negative files (can use glob syntax)
  -n FILENAME, --negative FILENAME
                        Files that have no annotations (can use glob syntax)
  --seed SEED           the seed to use for randomisation
  --label-separator SEPARATOR
                        the separator between the base filename and the label
  --labels LABEL [LABEL ...]
                        specifies the labels for each index
  --image-path-rel PATH
                        Relative path to image files from annotations
```

### FROM-ROI-OD
Reads image object-detection annotations in the ROI CSV-format

#### Domain(s):
- **Image Object-Detection Domain**

#### Options:
```
usage: from-roi-od [-I FILENAME] [-i FILENAME] [-N FILENAME] [-n FILENAME] [--seed SEED] [-e FORMAT FORMAT FORMAT] [--prefix READER_PREFIX] [--suffix READER_SUFFIX]

optional arguments:
  -I FILENAME, --inputs-file FILENAME
                        Files containing lists of input files (can use glob syntax)
  -i FILENAME, --input FILENAME
                        Input files (can use glob syntax)
  -N FILENAME, --negatives-file FILENAME
                        Files containing lists of negative files (can use glob syntax)
  -n FILENAME, --negative FILENAME
                        Files that have no annotations (can use glob syntax)
  --seed SEED           the seed to use for randomisation
  -e FORMAT FORMAT FORMAT, --extensions FORMAT FORMAT FORMAT
                        image format extensions in order of preference
  --prefix READER_PREFIX
                        the prefix for output filenames (default = '')
  --suffix READER_SUFFIX
                        the suffix for output filenames (default = '-rois.csv')
```

### FROM-SUBDIR-IC
Reads images from sub-directories named after their class labels.

#### Domain(s):
- **Image Classification Domain**

#### Options:
```
usage: from-subdir-ic [-I FILENAME] [-i FILENAME] [-N FILENAME] [-n FILENAME] [--seed SEED]

optional arguments:
  -I FILENAME, --inputs-file FILENAME
                        Files containing lists of input files (can use glob syntax)
  -i FILENAME, --input FILENAME
                        Input files (can use glob syntax)
  -N FILENAME, --negatives-file FILENAME
                        Files containing lists of negative files (can use glob syntax)
  -n FILENAME, --negative FILENAME
                        Files that have no annotations (can use glob syntax)
  --seed SEED           the seed to use for randomisation
```

### FROM-TF-OD
Reads image object-detection annotations in the TFRecords binary format

#### Domain(s):
- **Image Object-Detection Domain**

#### Options:
```
usage: from-tf-od [-I FILENAME] [-i FILENAME] [-N FILENAME] [-n FILENAME] [--seed SEED] [--mask-threshold THRESHOLD] [--sample-stride STRIDE]

optional arguments:
  -I FILENAME, --inputs-file FILENAME
                        Files containing lists of input files (can use glob syntax)
  -i FILENAME, --input FILENAME
                        Input files (can use glob syntax)
  -N FILENAME, --negatives-file FILENAME
                        Files containing lists of negative files (can use glob syntax)
  -n FILENAME, --negative FILENAME
                        Files that have no annotations (can use glob syntax)
  --seed SEED           the seed to use for randomisation
  --mask-threshold THRESHOLD
                        the threshold to use when calculating polygons from masks
  --sample-stride STRIDE
                        the stride to use when calculating polygons from masks
```

### FROM-VGG-OD
Reads image object-detection annotations in the VGG JSON-format

#### Domain(s):
- **Image Object-Detection Domain**

#### Options:
```
usage: from-vgg-od [-I FILENAME] [-i FILENAME] [-N FILENAME] [-n FILENAME] [--seed SEED]

optional arguments:
  -I FILENAME, --inputs-file FILENAME
                        Files containing lists of input files (can use glob syntax)
  -i FILENAME, --input FILENAME
                        Input files (can use glob syntax)
  -N FILENAME, --negatives-file FILENAME
                        Files containing lists of negative files (can use glob syntax)
  -n FILENAME, --negative FILENAME
                        Files that have no annotations (can use glob syntax)
  --seed SEED           the seed to use for randomisation
```


## Processor stage
### CHECK-DUPLICATE-FILENAMES
Causes the conversion stream to halt when multiple dataset items have the same filename

#### Domain(s):
- **Image Classification Domain**
- **Speech Domain**
- **Image Object-Detection Domain**
- **Image Segmentation Domain**

#### Options:
```
usage: check-duplicate-filenames
```

### COERCE-BOX
Converts all annotation bounds into box regions

#### Domain(s):
- **Image Object-Detection Domain**

#### Options:
```
usage: coerce-box
```

### COERCE-MASK
Converts all annotation bounds into polygon regions

#### Domain(s):
- **Image Object-Detection Domain**

#### Options:
```
usage: coerce-mask
```

### CONVERT-IMAGE-FORMAT
Converts images from one format to another

#### Domain(s):
- **Image Classification Domain**
- **Image Object-Detection Domain**
- **Image Segmentation Domain**

#### Options:
```
usage: convert-image-format -f FORMAT

optional arguments:
  -f FORMAT, --format FORMAT
                        format to convert images to
```

### DIMENSION-DISCARDER
Removes annotations which fall outside certain size constraints

#### Domain(s):
- **Image Object-Detection Domain**

#### Options:
```
usage: dimension-discarder [--max-area MAX_AREA] [--max-height MAX_HEIGHT] [--max-width MAX_WIDTH] [--min-area MIN_AREA] [--min-height MIN_HEIGHT] [--min-width MIN_WIDTH]

optional arguments:
  --max-area MAX_AREA   the maximum area of annotations to convert
  --max-height MAX_HEIGHT
                        the maximum height of annotations to convert
  --max-width MAX_WIDTH
                        the maximum width of annotations to convert
  --min-area MIN_AREA   the minimum area of annotations to convert
  --min-height MIN_HEIGHT
                        the minimum height of annotations to convert
  --min-width MIN_WIDTH
                        the minimum width of annotations to convert
```

### DISCARD-NEGATIVES
Discards negative examples (those without annotations) from the stream

#### Domain(s):
- **Image Classification Domain**
- **Speech Domain**
- **Image Object-Detection Domain**
- **Image Segmentation Domain**

#### Options:
```
usage: discard-negatives
```

### FILTER-LABELS
Filters detected objects down to those with specified labels.

#### Domain(s):
- **Image Object-Detection Domain**

#### Options:
```
usage: filter-labels [-l LABELS [LABELS ...]] [-r regexp]

optional arguments:
  -l LABELS [LABELS ...], --labels LABELS [LABELS ...]
                        labels to use
  -r regexp, --regexp regexp
                        regular expression for using only a subset of labels
```

### MAP-LABELS
Maps object-detection labels from one set to another

#### Domain(s):
- **Image Object-Detection Domain**

#### Options:
```
usage: map-labels [-m old=new]

optional arguments:
  -m old=new, --mapping old=new
                        mapping for labels, for replacing one label string with another (eg when fixing/collapsing labels)
```

### OD-TO-IS
Converts image object-detection instances into image segmentation instances

#### Domain(s):
- **Image Object-Detection Domain**

#### Options:
```
usage: od-to-is [--label-error] --labels LABEL [LABEL ...]

optional arguments:
  --label-error         whether to raise errors when an unspecified label is encountered (default is to ignore)
  --labels LABEL [LABEL ...]
                        specifies the labels for each index
```

### PASSTHROUGH
Dummy ISP which has no effect on the conversion stream

#### Domain(s):
- **Image Classification Domain**
- **Speech Domain**
- **Image Object-Detection Domain**
- **Image Segmentation Domain**

#### Options:
```
usage: passthrough
```

### REMOVE-CLASSES
Removes classes from classification/image-segmentation instances

#### Domain(s):
- **Image Classification Domain**
- **Image Segmentation Domain**

#### Options:
```
usage: remove-classes -c CLASS [CLASS ...]

optional arguments:
  -c CLASS [CLASS ...], --classes CLASS [CLASS ...]
                        the classes to remove
```

### STRIP-ANNOTATIONS
ISP which removes annotations from instances

#### Domain(s):
- **Image Classification Domain**
- **Speech Domain**
- **Image Object-Detection Domain**
- **Image Segmentation Domain**

#### Options:
```
usage: strip-annotations
```


## Sink stage
### TO-ADAMS-IC
Writes image classification annotations in the ADAMS report-format

#### Domain(s):
- **Image Classification Domain**

#### Options:
```
usage: to-adams-ic -c FIELD [--annotations-only] -o PATH [--split-names SPLIT NAME [SPLIT NAME ...]] [--split-ratios RATIO [RATIO ...]]

optional arguments:
  -c FIELD, --class-field FIELD
                        the report field containing the image class
  --annotations-only    skip the writing of data files, outputting only the annotation files
  -o PATH, --output PATH
                        output directory to write files to
  --split-names SPLIT NAME [SPLIT NAME ...]
                        the names to use for the splits
  --split-ratios RATIO [RATIO ...]
                        the ratios to use for the splits
```

### TO-ADAMS-OD
Writes image object-detection annotations in the ADAMS report-format

#### Domain(s):
- **Image Object-Detection Domain**

#### Options:
```
usage: to-adams-od [--annotations-only] -o PATH [--split-names SPLIT NAME [SPLIT NAME ...]] [--split-ratios RATIO [RATIO ...]]

optional arguments:
  --annotations-only    skip the writing of data files, outputting only the annotation files
  -o PATH, --output PATH
                        output directory to write files to
  --split-names SPLIT NAME [SPLIT NAME ...]
                        the names to use for the splits
  --split-ratios RATIO [RATIO ...]
                        the ratios to use for the splits
```

### TO-BLUE-CHANNEL-IS
Writes image segmentation files in the blue-channel format

#### Domain(s):
- **Image Segmentation Domain**

#### Options:
```
usage: to-blue-channel-is [--annotations-only] -o PATH [--split-names SPLIT NAME [SPLIT NAME ...]] [--split-ratios RATIO [RATIO ...]]

optional arguments:
  --annotations-only    skip the writing of data files, outputting only the annotation files
  -o PATH, --output PATH
                        the directory to write the annotation images to
  --split-names SPLIT NAME [SPLIT NAME ...]
                        the names to use for the splits
  --split-ratios RATIO [RATIO ...]
                        the ratios to use for the splits
```

### TO-COCO-OD
Writes image object-detection annotations in the MS-COCO JSON-format

#### Domain(s):
- **Image Object-Detection Domain**

#### Options:
```
usage: to-coco-od [--annotations-only] [--categories CATEGORY [CATEGORY ...]] [--category-output-file FILENAME] [--default-supercategory SUPERCATEGORY] [--error-on-new-category] [--license-name LICENSE_NAME] [--license-url LICENSE_URL] -o PATH [--pretty] [--sort-categories] [--split-names SPLIT NAME [SPLIT NAME ...]] [--split-ratios RATIO [RATIO ...]]

optional arguments:
  --annotations-only    skip the writing of data files, outputting only the annotation files
  --categories CATEGORY [CATEGORY ...]
                        defines the order of the categories
  --category-output-file FILENAME
                        file to write the categories into, as a simple comma-separated list
  --default-supercategory SUPERCATEGORY
                        the supercategory to use for pre-defined categories
  --error-on-new-category
                        whether unspecified categories should raise an error
  --license-name LICENSE_NAME
                        the license of the images
  --license-url LICENSE_URL
                        the license of the images
  -o PATH, --output PATH
                        output file to write annotations to (images are placed in same directory)
  --pretty              whether to format the JSON annotations file with indentation
  --sort-categories     whether to put the categories in alphabetical order
  --split-names SPLIT NAME [SPLIT NAME ...]
                        the names to use for the splits
  --split-ratios RATIO [RATIO ...]
                        the ratios to use for the splits
```

### TO-COMMON-VOICE-SP
Writes speech transcriptions in the Mozilla Common-Voice TSV-format

#### Domain(s):
- **Speech Domain**

#### Options:
```
usage: to-common-voice-sp [--annotations-only] -o PATH [--split-names SPLIT NAME [SPLIT NAME ...]] [--split-ratios RATIO [RATIO ...]]

optional arguments:
  --annotations-only    skip the writing of data files, outputting only the annotation files
  -o PATH, --output PATH
                        the filename of the TSV file to write the annotations into
  --split-names SPLIT NAME [SPLIT NAME ...]
                        the names to use for the splits
  --split-ratios RATIO [RATIO ...]
                        the ratios to use for the splits
```

### TO-FESTVOX-SP
Writes speech transcriptions in the Festival FestVox format

#### Domain(s):
- **Speech Domain**

#### Options:
```
usage: to-festvox-sp [--annotations-only] -o PATH [--split-names SPLIT NAME [SPLIT NAME ...]] [--split-ratios RATIO [RATIO ...]]

optional arguments:
  --annotations-only    skip the writing of data files, outputting only the annotation files
  -o PATH, --output PATH
                        the filename of the FestVox file to write the annotations into
  --split-names SPLIT NAME [SPLIT NAME ...]
                        the names to use for the splits
  --split-ratios RATIO [RATIO ...]
                        the ratios to use for the splits
```

### TO-INDEXED-PNG-IS
Writes image segmentation files in the indexed-PNG format

#### Domain(s):
- **Image Segmentation Domain**

#### Options:
```
usage: to-indexed-png-is [--annotations-only] -o PATH [--split-names SPLIT NAME [SPLIT NAME ...]] [--split-ratios RATIO [RATIO ...]]

optional arguments:
  --annotations-only    skip the writing of data files, outputting only the annotation files
  -o PATH, --output PATH
                        the directory to write the annotation images to
  --split-names SPLIT NAME [SPLIT NAME ...]
                        the names to use for the splits
  --split-ratios RATIO [RATIO ...]
                        the ratios to use for the splits
```

### TO-LAYER-SEGMENTS-IS
Writes the layer-segments image-segmentation format to disk

#### Domain(s):
- **Image Segmentation Domain**

#### Options:
```
usage: to-layer-segments-is [--annotations-only] [--label-separator SEPARATOR] -o PATH [--split-names SPLIT NAME [SPLIT NAME ...]] [--split-ratios RATIO [RATIO ...]]

optional arguments:
  --annotations-only    skip the writing of data files, outputting only the annotation files
  --label-separator SEPARATOR
                        the separator between the base filename and the label
  -o PATH, --output PATH
                        the directory to write the annotation images to
  --split-names SPLIT NAME [SPLIT NAME ...]
                        the names to use for the splits
  --split-ratios RATIO [RATIO ...]
                        the ratios to use for the splits
```

### TO-ROI-OD
Writes image object-detection annotations in the ROI CSV-format

#### Domain(s):
- **Image Object-Detection Domain**

#### Options:
```
usage: to-roi-od [-d WIDTH HEIGHT] [--annotations-only] [--comments COMMENTS [COMMENTS ...]] -o PATH [--size-mode] [--split-names SPLIT NAME [SPLIT NAME ...]] [--split-ratios RATIO [RATIO ...]] [--prefix WRITER_PREFIX] [--suffix WRITER_SUFFIX]

optional arguments:
  -d WIDTH HEIGHT, --image-dimensions WIDTH HEIGHT
                        image dimensions to use if none can be inferred
  --annotations-only    skip the writing of data files, outputting only the annotation files
  --comments COMMENTS [COMMENTS ...]
                        comments to write to the beginning of the ROI file
  -o PATH, --output PATH
                        output directory to write files to
  --size-mode           writes the ROI files with x,y,w,h headers instead of x0,y0,x1,y1
  --split-names SPLIT NAME [SPLIT NAME ...]
                        the names to use for the splits
  --split-ratios RATIO [RATIO ...]
                        the ratios to use for the splits
  --prefix WRITER_PREFIX
                        the prefix for output filenames (default = '')
  --suffix WRITER_SUFFIX
                        the suffix for output filenames (default = '-rois.csv')
```

### TO-SUBDIR-IC
Writes images to sub-directories named after their class labels.

#### Domain(s):
- **Image Classification Domain**

#### Options:
```
usage: to-subdir-ic -o PATH [--split-names SPLIT NAME [SPLIT NAME ...]] [--split-ratios RATIO [RATIO ...]]

optional arguments:
  -o PATH, --output PATH
                        the directory to store the class directories in
  --split-names SPLIT NAME [SPLIT NAME ...]
                        the names to use for the splits
  --split-ratios RATIO [RATIO ...]
                        the ratios to use for the splits
```

### TO-TF-OD
Writes image object-detection annotations in the TFRecords binary format

#### Domain(s):
- **Image Object-Detection Domain**

#### Options:
```
usage: to-tf-od [--dense] -o PATH [-p FILENAME] [-s FILENAME [FILENAME ...]] [--split-names SPLIT NAME [SPLIT NAME ...]] [--split-ratios RATIO [RATIO ...]]

optional arguments:
  --dense               outputs masks in the dense numerical format instead of PNG-encoded
  -o PATH, --output PATH
                        name of output file for TFRecords
  -p FILENAME, --protobuf FILENAME
                        for storing the label strings and IDs
  -s FILENAME [FILENAME ...], --shards FILENAME [FILENAME ...]
                        additional shards to write to
  --split-names SPLIT NAME [SPLIT NAME ...]
                        the names to use for the splits
  --split-ratios RATIO [RATIO ...]
                        the ratios to use for the splits
```

### TO-VGG-OD
Writes image object-detection annotations in the VGG JSON-format

#### Domain(s):
- **Image Object-Detection Domain**

#### Options:
```
usage: to-vgg-od [--annotations-only] -o PATH [--pretty] [--split-names SPLIT NAME [SPLIT NAME ...]] [--split-ratios RATIO [RATIO ...]]

optional arguments:
  --annotations-only    skip the writing of data files, outputting only the annotation files
  -o PATH, --output PATH
                        output file to write annotations to (images are placed in same directory)
  --pretty              whether to format the JSON annotations file with indentation
  --split-names SPLIT NAME [SPLIT NAME ...]
                        the names to use for the splits
  --split-ratios RATIO [RATIO ...]
                        the ratios to use for the splits
```


