# Contributing to Synthizer-python

Synthizer-python is open to pull requests for bug fixes and new features.
Please create issues discussing new features before starting work on them, in
case they need to wait, shouldn't be done, or will be more complicated than you
might think.

## Licensing

This project is under the [unlicense](./LICENSE).  Please include the folllowing
at the bottom of your PR comment:

```
I have read CONTRIBUTING.md, am the sole contributor to this pull request, and license my contributions under the Unlicense.
```

If there's multiple contributors to your PR, let me know in the PR. I'll need
them to all have GitHub accounts, and to leave a comment to the effect of them
agreeing that their contribution is under the unlicense as well.

We might make this more formal later, but the unlicense is liberal enough to
even allow relicensing, so for the time being there's no CLA.

## Overview Of Updating The Bindings

Let's say that Synthizer has added some new amazing feature and you want to add
support for the Python bindings.  The general procedure is as follows:

### Generate pxd files from autopxd2

Install [autopxd2](https://github.com/gabrieldemarmiesse/python-autopxd2).  This
is a utility that can generate Cython pxd files from C headers.

From Linux (or, on Windows, WSL), run generate-cython.sh in the root of this
repository.  This will generate some pxd files in the right places.
### Add nogil

The pxd files for Cython generated in the step above are now missing some nogil
statements.  Typically this is on `syz_shutdown` and all the functions for
creating buffers.  You need to add them back.  Forking autopxd2 to just make
everything nogil is sort of on the to-do list but probably won't happen soon.

If you miss one that's okay: Cython will refuse to compile and tell you which
one it is.

### Change synthizer.pyx

This is where the main binding lives.  We can't split the file because Cython
doesn't like that; if we do, we get more than one DLL and that's really not so
great.

### Install for Development

`python setup.py develop` is the magic command here.  You'll want to do this in
a dedicated virtualenv because sometimes Python likes to be buggy about
uninstalling/updating and you might have to wipe it out.

If you think a build should have happened but it seems like setup.py didn't do
anything, it probably didn't.  In particular this likes to happen when
re-vendoring Synthizer.  To fix this, delete all the extra files from the build,
e.g. `dist`.

### Update or Produce an Example

Synthizer isn't the sort of thing that can have automated tests, so we do our
testing around examples.  We also don't have a good story about docs for the
Python bindings (unless you're volunteering to keep them up to date).  To that
end new features should come with at least a simple example.

### Update synthizer.pyi

These are the Muypy type stubs.

### Open a PR and review

This is thetraditional process.  We do have CI and your changes must pass it.
