#!/usr/bin/env python3
"""setup.py for KBTogglr - install overridden and uninstall added"""
import os
import sys

import setuptools

import kbtogglr

sys.path.insert(0, os.path.abspath('kbtogglr'))  # noqa
from src.install.uninstaller import Uninstall
from src.install.installer import Install


def readme():
    """Add readme to package metadata"""
    with open("README.rst", "r") as file:
        return file.read()


setuptools.setup(
    name=kbtogglr.__project__,
    version=kbtogglr.__version__,
    license=kbtogglr.__license__,
    author=kbtogglr.__author__,
    author_email=kbtogglr.__email__,
    description=(
        "Toggle keyboard on and off - useful for using usb keyboards"
    ),
    long_description=readme(),
    long_description_content_type="text/x-rst",
    url="https://github.com/jshwi/kbtogglr",
    classifiers=[
        "Programming Language :: Python :: 3.8",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    py_modules=["object_colors"],
    packages=setuptools.find_packages(exclude=("tests",)),
    include_package_data=True,
    zip_safe=True,
    install_requires=["pytest"],
    python_requires='>=3.8',
    cmdclass={"install": Install, "uninstall": Uninstall}
)
