from os import PathLike, path, remove
from shutil import rmtree
from typing import Union

from setuptools import Command

from src.install.helpers import print_color
from src import paths


class Uninstaller:
    """Uninstaller methods"""

    def __init__(self) -> None:
        self.env = paths.ENV

    @staticmethod
    def __rm_dir(key: str, dir_: Union[bytes, str, PathLike]) -> None:
        if path.isdir(dir_):
            print_color(f"  - Removing {key}:")
            rmtree(dir_)
            print(f"    Removed {dir_}")

    @staticmethod
    def __rm_file(key: str, file: Union[bytes, str, PathLike]) -> None:
        if path.isfile(file) or path.islink(file):
            print_color(f"  - Removing {key}:")
            remove(file)
            print(f"    Removed {file}")

    def run_uninstaller(self) -> None:
        """Remove files or directories if they exist and then announce
        result
        """
        attrs = {
            "launcher": "desktop",
            "status file": "save_file",
            "package": "kbtogglr",
            "executable": "exec"
        }
        print_color("\n  Removing KBTogglr", bold=True)
        for key, attr in attrs.items():
            value = self.env[attr]
            self.__rm_dir(key, value)
            self.__rm_file(key, value)
        print_color("\n  KBTogglr uninstalled successfully", bold=True)


class Uninstall(Command):  # noqa
    """Add uninstall command class to `setup.py`"""

    user_options = []

    # noinspection PyAttributeOutsideInit
    def initialize_options(self) -> None:
        """Abstract method that is required to be overwritten"""

    def finalize_options(self) -> None:
        """Abstract method that is required to be overwritten"""

    @staticmethod
    def run() -> None:
        """Uninstall KBTogglr"""
        uninstaller = Uninstaller()
        uninstaller.run_uninstaller()
