import os
import os.path
import shutil
import stat
import subprocess

from setuptools import Extension, setup
from Cython.Build import cythonize
from Cython.Compiler import Options

VERSION = "0.12.6"

# A helper for rmtree. On Windows, read-only files can't be deleted by rmtree, so we make them not readonly.
def handle_remove_readonly(func, path, exc):
    os.chmod(path, stat.S_IRWXU | stat.S_IRWXG | stat.S_IRWXO)  # 0777
    func(path)

extension_args = {}
Options.language_level = 3

# scikit-build isn't always present.
from skbuild import cmaker

# we can go via scikit-build to try to run CMake. This is reliable enough on Linux and Mac, but will probably
# give people trouble on Windows, thus us publishing wheels.
# Find this file:
root_dir = os.path.split(os.path.abspath(__file__))[0]
vendored_dir = os.path.join(root_dir, "synthizer-vendored")
os.chdir(root_dir)

synthizer_lib_dir = ""
if 'CI_SDIST' not in os.environ:
    # Configure and build Synthizer itself.
    cmake = cmaker.CMaker()
    # Force Ninja on all platforms. This lets us work on Windows reliably if run
    # from an MSVC shell, where reliably means fail noisily and obviously at the
    # beginning if the world is insane.
    cmake.configure(
        cmake_source_dir=vendored_dir,
        generator_name="Ninja",
        clargs=[
            "-DCMAKE_BUILD_TYPE=Release",
            "-DCMAKE_MSVC_RUNTIME_LIBRARY=MultiThreaded",
            "-DCMAKE_POSITION_INDEPENDENT_CODE=TRUE",
            "-DSYZ_INTEGRATING=ON",
        ],
    )
    cmake.make()
    # what actually happens here is that Synthizer only installs one path. It is
    # unfortunately the case that skbuild is making architecture specific
    # directories so, instead of guessing, just grab it.
    synthizer_lib_dir = os.path.split(os.path.abspath(cmake.install()[0]))[0]
extension_args = {
    "include_dirs": [os.path.join(vendored_dir, "include")],
    "library_dirs": [synthizer_lib_dir],
    "libraries": ["synthizer"],
}

extensions = [
    Extension("synthizer.synthizer", ["synthizer/synthizer.pyx"], **extension_args),
]

setup(
    name="synthizer",
    version=VERSION,
    author="Synthizer Developers",
    author_email="ahicks@ahicks.io",
    url="https://synthizer.github.io",
    ext_modules=cythonize(extensions, language_level=3),
    zip_safe=False,
    include_package_data=True,
    packages=["synthizer"],
    package_data={
        "synthizer": ["*.pyx", "*.pxd", "*.pyi", "py.typed"],
    },
)
