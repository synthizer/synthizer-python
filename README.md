# Synthizer Python Bindings

These are the [Synthizer](https://github.com/synthizer/synthizer) Python
bindings.  Se the Synthizer manual for more details and example usage.

## Installing From This Repository

You probably want the Pypi version, which will just `pip install` for you
without a problem.  But if you want to install from this repository it's sadly
more involved than just depending on it, since the Python bindings need to
produce a vendored version of Synthizer itself.  it's possible to get source
distributions and wheels from the [CI
runs](https://github.com/synthizer/synthizer-python/actions), or you can follow
the ofllowing procedure:

- Clone this repo including the submodule: `git clone --recursive
  https://github.com/synthizer/synthizer-python`
- From the root of this repo, `python synthizer-c/vendor.py synthizer-vendored`
- Then `python setup.py install` or `bdist_wheel` or whatever.

## Maintainers Wanted

I (@ahicks92) don't have the bandwidth to maintain all bindings we might want
and have primarily moved on to Rust.  Consequently the Python bindings can be
expected to lag behind Synthizer proper unless maintainers step up.  You'll need
to know C and Cython to get anywhere fast.  Otherwise I'll just be adding to
this as I have extra time.  How this works is as follows:

- You decide to add something.
- if whatever you're adding is going to take more than 5 minutes and/or you
  don't want to be told no after the fact, open an issue and propose a design.
  - Or if someone else made an issue, use that one.
- add the thing and submit a PR.
- I review your PR.
- We land your PR.
- anyone who needs to use Synthizer without a release can use the instructions
  above for installing from the repository.
- At some point, usually around the time of a Synthizer release, I tag a release
  here as well and your changes go out to Pypi.
