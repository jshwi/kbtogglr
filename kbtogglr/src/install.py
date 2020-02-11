#!/usr/bin/env python3
"""Install or Uninstall KBTogglr with `python setup.py install` or
`python setup.py uninstall`
"""
from configparser import ConfigParser
from contextlib import redirect_stdout
from os import path, symlink, chmod, remove, PathLike, makedirs
import os
from shutil import copytree, rmtree
from typing import Union

from setuptools import Command
from setuptools.command.install import install as _install

from src.toggle import Toggle


class Desktop(Toggle):
    """Configure environment specific attributes for `.desktop_` file"""

    def __init__(self) -> None:
        super().__init__()
        self.local = path.join(self.home, ".local")
        self.share = path.join(self.local, "share")
        self.bin = path.join(self.local, "bin")
        self.exec = path.join(self.bin, "kbtogglr")
        self.template = path.join(self.package, "lib", "template.desktop")
        self.desktop = path.join(
            self.local, "share", "applications", "kbtogglr.desktop"
        )
        self.config = ConfigParser()

    @staticmethod
    def print_color(str_: str, bold=False) -> None:
        print(f"\u001b[{int(bold)};{33};40m{str_}\u001b[0;0m")

    def __configure_config(self) -> None:
        self.config.optionxform = str

    def __read_template(self) -> None:
        self.config.read(self.template)

    def __configure_exec(self) -> None:
        self.print_color("  - Configuring executable path:")
        print(f"    Exec = \"{self.exec}\"")
        self.config["Desktop Entry"]["Exec"] = self.exec

    def __configure_icon(self) -> None:
        self.print_color("  - Configuring icon location:")
        icon = path.join(self.images, "icon.png")
        print(f"    Icon = \"{icon}\"")
        self.config["Desktop Entry"]["Icon"] = icon

    def __write_desktop_file(self) -> None:
        self.print_color(f"  - Writing `kbtogglr.desktop`:")
        print(f"    {self.template} -> {self.desktop}")
        with open(self.desktop, "w") as file:
            self.config.write(file, space_around_delimiters=False)

    def __change_app_mode(self) -> None:
        chmod(self.desktop, 0o644)

    def write_launcher(self) -> None:
        """Write launcher data to file and then run chmod 644 on it"""
        self.__write_desktop_file()
        self.__change_app_mode()

    def run_desktop(self) -> None:
        """Run methods that will configure and install an application
        launcher for use with gui
        """
        self.__configure_config()
        self.__read_template()
        self.__configure_exec()
        self.__configure_icon()
        self.write_launcher()


class Installer(Desktop):
    """Installer methods"""

    def __init__(self) -> None:
        super().__init__()
        self.kbtogglr = path.join(self.home, ".kbtogglr")
        self.dot_package = path.join(self.kbtogglr, "kbtogglr")
        self.main = path.join(self.dot_package, "__main__.py")

    def __cp_repo(self) -> None:
        if not path.isdir(self.kbtogglr):
            self.print_color("  - Installing package:")
            print(f"    {self.repo} -> {self.kbtogglr}")
            copytree(self.repo, self.kbtogglr)

    def __change_main_mode(self) -> None:
        chmod(self.main, 0o755)

    def __make_bin(self) -> None:
        if not path.isdir(self.bin):
            makedirs(self.bin)

    def __symlink_exec(self) -> None:
        if not path.exists(self.exec):
            self.print_color("  - Installing executable:")
            print(f"    {self.main} -> {self.exec}")
            symlink(self.main, self.exec)

    def run_installer(self) -> None:
        """Run installer methods"""
        self.print_color("\n  Installing KBTogglr", bold=True)
        self.__make_bin()
        self.__cp_repo()
        self.__symlink_exec()
        self.__change_main_mode()
        self.print_color("\n  Installing launcher", bold=True)
        self.run_desktop()
        self.print_color("\n  KBTogglr installed successfully")


class Uninstaller(Installer):
    """Uninstaller methods"""

    def __init__(self) -> None:
        super().__init__()

    def __rm_dir(self, key: str, dir_: Union[bytes, str, PathLike]) -> None:
        if path.isdir(dir_):
            self.print_color(f"  - Removing {key}:")
            rmtree(dir_)
            print(f"    Removed {dir_}")

    def __rm_file(self, key: str, file: Union[bytes, str, PathLike]) -> None:
        if path.isfile(file) or path.islink(file):
            self.print_color(f"  - Removing {key}:")
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
        self.print_color("\n  Removing KBTogglr", bold=True)
        for key, attr in attrs.items():
            value = self.__dict__[attr]
            self.__rm_dir(key, value)
            self.__rm_file(key, value)
        self.print_color("\n  KBTogglr uninstalled successfully", bold=True)


def suppress_stdout(func):
    def wrapper(*a, **ka):
        with open(os.devnull, 'w') as devnull:
            with redirect_stdout(devnull):
                func(*a, **ka)
    return wrapper


# noinspection PyPep8Naming
class Install(Command):  # noqa
    """Inherit install from setuptools and override run()"""

    def __init__(self, dist, **kw):
        super().__init__(dist, **kw)
        self.dist = dist
        self.package = None

    user_options = _install.user_options + [("package", "p", None)]

    def initialize_options(self) -> None:
        """Abstract method that is required to be overwritten"""
        self.package = None

    def finalize_options(self) -> None:
        """Abstract method that is required to be overwritten"""

    @suppress_stdout
    def _install(self):
        Install(self.dist)

    def run(self) -> None:
        """Install KBTogglr"""
        if self.package:
            self._install()
        Installer().run_installer()


# noinspection PyPep8Naming
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
        Uninstaller().run_uninstaller()
