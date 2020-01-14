Changelog
=========

0.0.1 (2019-12-04)
-------------------

- Initial release

0.0.2 (2019-12-09)
-------------------

- Can now work with images that contain no annotations.

0.0.3 (2019-12-16)
------------------

- Changed --coerce option to --force.
- Tensorflow is no longer a dependency in setup.py as can work with
  tensorflow or tensorflow-gpu.
- TFRecords format can now handle polygon-mask annotations.

0.0.4 (2020-01-15)
------------------

- Modified requirements to include Cython as this is required in later versions
  of pycocotools. Moved pycocotools to end of dependency list to ensure all
  requirements are met before installation.
