Pypi
====

Preparation:
* increment version in `setup.py`
* add new changelog section in `CHANGES.rst`
* update the plugin documentation on the wai.annotations manual
  
  https://github.com/waikato-ufdl/wai-annotations-manual#updating-plugin-documentation
  
* commit/push all changes

Commands for releasing on pypi-waikato (requires twine >= 1.8.0):

```
  rm -r dist wai.annotations.egg-info
  python setup.py clean sdist
  twine upload dist/*
```


Github
======

Steps:
* start new release (version: `vX.Y.Z`)
* enter release notes, i.e., significant changes since last release
* upload `wai.annotations-X.Y.Z.tar.gz` previously generated with `setup.py`
* publish

