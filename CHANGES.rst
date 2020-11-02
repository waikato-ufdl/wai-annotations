Changelog
=========

0.5.3 (2020-11-03)
------------------

- Added ability to provide a source iterable when using `iterate_files`.
- `ConversionPipelineBuilder` now works with any combination of sources, processors and sinks.
- Data elements now are only referred to by their base filename.

0.5.2 (2020-11-02)
------------------

- Added the layer-segments image-segmentation format.
- Added the `od-to-is` cross-domain converter.
- Bug fixes.

0.5.1 (2020-10-30)
------------------

- Fixed bug in calculating output directory from command-line option.
- Added `strip-annotations` ISP.
- Stopped COCO/ROI/VGG image object-detection formats from writing negative annotations.
- Fixed bug in coercions where negatives instances weren't being handled correctly.
- Added `--dense` option to `to-tf-od` which encodes masks in the dense numerical format.

0.5.0 (2020-10-27)
------------------

- Refactor of the internal structure to aid in debugging.
- All input/output formats now end in the short-code of their domain.

0.4.7 (2020-09-03)
------------------

- Fixed bug where `--category-output-file` was being written to an arbitrary location.

0.4.6 (2020-08-05)
------------------

- Added --category-output-file option to to-coco format for writing the categories to a simple
  comma-separated text file.
- Added the subdir image classification format.
- Added the ADAMS image classification format.
- Refactored label-mapping, image format conversion and label filtering into their own
  ISPs (were options on object detection readers/writers).
- Better error messages when domains are incorrectly matched.
- Upgraded wai.common requirement to fix bug with file iteration.

0.4.5 (2020-08-03)
------------------

- Made help more helpful.
- Added macros, which allow for simple command-line argument substitution.
- Improved logging during split-writes. More improvements to come.

0.4.4 (2020-07-29)
------------------

- Separated base reader/writer functionality into abstract bases which don't assume
  local disk access.

0.4.3 (2020-07-28)
------------------

- Added new option to the MS-COCO format to sort the categories.

0.4.2 (2020-07-28)
------------------

- Added new options to the MS-COCO format for pre-specifying the categories to expect.

0.4.1 (2020-07-27)
------------------

- Added domain information to the `--list-plugins` command.
- Basic support for speech annotations, including CommonVoice and FestVox formats.
- Added `--debug` global flag to aid in debugging.
- Added file_iterator method to conversion chains, allowing iteration over the converted file-data.
- Fixed dependency error on installation from PyPI caused by pycocotools.
- Bug fixes.

0.4.0 (2020-07-02)
------------------

- Major restructure to introduce domains other than object-detection in images.

0.3.6 (2020-06-22)
------------------

- Modified numpy/pycocotools requirements to work with EfficientDet.
- Added sha256, is_crowd and area features to TFRecords format to work with EfficientDet.
- Fixed bug where full set of TFRecord shard files wasn't being generated.

0.3.5 (2020-04-03)
------------------

- Added InputChain and OutputChain classes, encapsulating the stages of input and output respectively.
- Modified parsing so that users can create "main-like" CLI interfaces.
- Bug fixes.

0.3.4 (2020-03-31)
------------------

- Updated requirement for wai.common to v0.0.31.
- Updated requirement for wai.bynning to v0.0.2.

0.3.3 (2020-03-27)
------------------

- Added support for BMP-format images.
- Added ``--convert-image`` option to convert images to a given image-format.

0.3.2 (2020-03-24)
------------------

- Added ``--split-names`` and ``--split-ratios`` options for creating splits in the
  dataset.
- Added ``--seed`` option for randomising file-read order.

0.3.1 (2020-03-18)
------------------

- Bug fix where plugin registry was being recreated every run.
- Bug fix where previous registry incarnation was being loaded instead of new version.

0.3.0 (2020-03-18)
------------------

- Converted formats to use a plug-in system so other libraries can define their own formats.

0.2.3 (2020-03-17)
------------------

- Upgraded wai.common requirement to v0.0.28.
- Separated main settings from library settings.
- Changed ``--include-zero-area`` flag to min/max width/height/area flags.
- Added ``--comments`` option for ROI writer to insert comments at the beginning
  of written files.
- Input directories read all contained files ending in ``.report`` when using ``adams`` format.
- Added ``--sample-stride`` option to tfrecords input which sub-samples the mask when generating
  the polygon for speed increase.
- Added ``--mask-threshold`` option to tfrecords input which sets the probability to consider
  the mask inside the polygon.
- Internal format is now an object rather than a tuple.
- Added ``--size-mode`` flag to ROI format which writes ROI files with x,y,w,h headers rather
  than x0,y0,x1,y1 headers.

0.2.2 (2020-03-11)
------------------

- Upgraded wai.common requirement to v0.0.26.

0.2.1 (2020-03-11)
------------------

- VGG/COCO formats can now take a ``--pretty`` flag to pretty-print their JSON annotations.
- Upgraded wai.common requirement to v0.0.25.
- `image_utils.lists_to_polygon` method converts lists of X and Y coordinates into a `planar.Polygon`
- `image_utils.polygon_to_bbox` method returns the x0,y0,x1,y1 coordinates of the bounding box around
  the supplied `planar.Polygon` object

0.2.0 (2020-03-06)
------------------

- Conversions now automatically discard annotations with zero area, can be reverted
  with ``--include-zero-area`` flag.
- `image_utils.mask_to_polygon` can now work with a view of the mask instead of
  the full mask to speed up the polygon detection
- Modified utilities for getting labels/prefixes to be able to specify a default value.
- Upgraded wai.common requirement to v0.0.24.
- Added requirement for wai.json v0.0.4.

0.1.4 (2020-02-18)
------------------

- Added compatibility layer for Tensorflow V1.
- Now ensures Tensorflow is in eager execution mode.

0.1.3 (2020-02-12)
------------------

- Upgraded wai.common requirement to v0.0.22.

0.1.2 (2020-01-24)
------------------

- Fixed default filename for ROI format ("-rois.csv" rather than "-roi.csv").
- Added the ability to specify a prefix and suffix for reading/writing ROI files.
- Logging changes.
- Moved utilities for each format into their own sub-package.
- Added reader options to read input files from list files.

0.1.1 (2020-01-23)
------------------

- Separated command-line option parsing from io/converter classes so that imports
  unique to specific formats are not required unless using that format.
- Refactoring of package structure.
- Added logging of when files are being written.
- Conversion to COCO format now report polygon mask area, rather than just bounding-
  box area.
- Added support for non-standard keywords to the ROI format.

0.1.0 (2020-01-22)
------------------

- Added the ability to specify inputs by glob syntax, and also specify negative
  images with no annotations.
- Added utility functions for images (image_to_numpyarray, remove_alpha_channel)
  and for masks (mask_to_polygon, polygon_to_minrect, polygon_to_lists) in module wai.annotations.image_utils
- Added --extensions option to control the search order for associated images.
- Added --verbosity flag to control logging verbosity.
- Added polygon mask support to the ROI format.

0.0.4 (2020-01-15)
------------------

- Modified requirements to include Cython as this is required in later versions
  of pycocotools. Moved pycocotools to end of dependency list to ensure all
  requirements are met before installation.

0.0.3 (2019-12-16)
------------------

- Changed --coerce option to --force.
- Tensorflow is no longer a dependency in setup.py as can work with
  tensorflow or tensorflow-gpu.
- TFRecords format can now handle polygon-mask annotations.

0.0.2 (2019-12-09)
-------------------

- Can now work with images that contain no annotations.

0.0.1 (2019-12-04)
-------------------

- Initial release
