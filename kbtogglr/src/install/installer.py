import os
from shutil import copytree

from setuptools import Command
from setuptools.command.install import install as _install

from src.install.desktop import Desktop
from src.install.helpers import print_color, suppress_stdout
from src import paths


class Installer(Desktop):
    """Installer methods"""

    def __init__(self) -> None:
        super().__init__()
        self.env = paths.ENV

    def __cp_repo(self) -> None:
        if not os.path.isdir(self.env["kbtogglr"]):
            print_color("  - Installing package:")
            print(f"    {self.env['repo']} -> {self.env['kbtogglr']}")
            copytree(self.env["repo"], self.env["kbtogglr"])

    def __change_main_mode(self) -> None:
        os.chmod(self.env["main"], 0o755)

    def __make_bin(self) -> None:
        if not os.path.isdir(self.env["bin"]):
            os.makedirs(self.env["bin"])

    def __symlink_exec(self) -> None:
        if not os.path.exists(self.env["exec"]):
            print_color("  - Installing executable:")
            print(f"    {self.env['main']} -> {self.env['exec']}")
            os.symlink(self.env["main"], self.env["exec"])

    def run_installer(self) -> None:
        """Run installer methods"""
        print_color("\n  Installing KBTogglr", bold=True)
        self.__make_bin()
        self.__cp_repo()
        self.__symlink_exec()
        self.__change_main_mode()
        print_color("\n  Installing launcher", bold=True)
        self.run_desktop()
        print_color("\n  KBTogglr installed successfully", bold=True)


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
        installer = Installer()
        installer.run_installer()
