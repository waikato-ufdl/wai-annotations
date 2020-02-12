Changelog
=========

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
