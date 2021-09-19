#!/usr/bin/env bash
set -ex

# This generates cython .pxd definitions.
# To use, pip install autopxd2 in  virtualenv then run the script.
# We don't run this as part of CI or the build process.
# You can ignore pragma once in main file warnings.

cd synthizer-c/include
autopxd synthizer.h > ../../synthizer/synthizer.pxd
autopxd synthizer_constants.h > ../../synthizer/synthizer_constants.pxd
