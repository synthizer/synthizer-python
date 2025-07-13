# Synthizer Python Bindings

These are the [Synthizer](https://github.com/synthizer/synthizer) Python
bindings.  Se the Synthizer manual for more details and example usage.

## WARNING: UINMAINTAINED

This is unmaintained software. Issues will be ignored. PRs will be closed without merging.  If it is of use to you, please feel free to fork.

## Installing From This Repository

You probably want the Pypi version, which will just `pip install` for you
without a problem.  But if you want to install from this repository it's sadly
more involved than just depending on it, since the Python bindings need to
produce a vendored version of Synthizer itself.  It's possible to get source
distributions and wheels from the [CI
runs](https://github.com/synthizer/synthizer-python/actions), or you can follow
the following procedure:

- Clone this repo including the submodule: `git clone --recursive
  https://github.com/synthizer/synthizer-python`
- From the root of this repo, `python synthizer-c/vendor.py synthizer-vendored`
- Then `python setup.py install` or `bdist_wheel` or whatever.

