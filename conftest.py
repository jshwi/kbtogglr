#!/usr/bin/env python3
from os import path
from typing import List

from pytest import fixture

from kbtogglr.src import install


def make_path_temp(tmpdir: fixture, obj: install, attrs: List[str]) -> install:
    for attr in attrs:
        path_ = path.join(tmpdir, obj.__dict__[attr])
        obj.__dict__[attr] = path_
    return obj


@fixture
def desktop_(tmpdir: fixture) -> install:
    desktop_attrs = ["desktop", "exec", "images"]
    desktop_fixture = install.Desktop()
    print()
    return make_path_temp(tmpdir, desktop_fixture, desktop_attrs)


@fixture
def installer_(tmpdir: fixture) -> install:
    installer_attrs = ["repo", "main", "kbtogglr", "bin"]
    installer_fixture = install.Installer()
    return make_path_temp(tmpdir, installer_fixture, installer_attrs)


@fixture
def uninstaller_(tmpdir: fixture) -> install:
    uninstaller_attrs = ["kbtogglr", "save_file", "package", "exec"]
    uninstaller_fixture = install.Uninstaller()
    return make_path_temp(tmpdir, uninstaller_fixture, uninstaller_attrs)


@fixture
def run_desktop(desktop_: install) -> None:
    desktop_.run_desktop()


@fixture
def run_installer(installer_: install) -> None:
    installer_.run_installer()


@fixture
def run_uninstaller(uninstaller_: install) -> None:
    uninstaller_.run_uninstaller()
