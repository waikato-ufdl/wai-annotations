Pypi
====

Preparation:
* increment version in `setup.py`
* add new changelog section in `CHANGES.rst`
  
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


Manual
======

Update the plugin documentation of the wai.annotations manual
  
  https://github.com/waikato-ufdl/wai-annotations-manual#updating-plugin-documentation


Docker
======

* Copy sub-folder in [docker](docker) directory with new version number
* Adjust versions in:

  * `README.md`
  * `Dockerfile`
  * `bash.bashrc`
  
* Test and adjust `Dockerfile` if necessary
* Add link to new version in [docker/README.md](docker/README.md)
* Build and deploy docker image to local registry and docker hub
