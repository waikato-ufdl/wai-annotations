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
* Ensure that [docker/latest/Dockerfile](docker/latest/Dockerfile) uses all the wai.annotations repos


Scripts
=======

* Ensure that [install.sh](install.sh) contains all the wai.annotations repos.


README.md
=========

* Ensure that [README.md](README.md) points to all the github repositories.


Manual
======

* Update the list of available plugins in `docs/install.md`

* Update the plugin documentation of the wai.annotations manual
  
  https://github.com/waikato-ufdl/wai-annotations-manual#updating-plugin-documentation

* Update the list of available docker images in `docs/docker.md`
