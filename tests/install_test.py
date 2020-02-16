#!/usr/bin/env python3
from os import path, stat
from stat import ST_MODE

from pytest import fixture

from conftest import prepare_obj, environ
from src.install.desktop import Desktop
from src.install.installer import Installer
from src.install.uninstaller import Uninstaller


class TestDesktop:

    def test_isfile_desktop(self, tmpdir: fixture):
        env = environ(tmpdir)
        desktop_ = prepare_obj(env, Desktop)
        desktop_.run_desktop()
        assert path.isfile(env["desktop"])

    def test_mode_desktop(self, tmpdir: fixture):
        env = environ(tmpdir)
        desktop_ = prepare_obj(env, Desktop)
        desktop_.run_desktop()
        assert oct(stat(env["desktop"])[ST_MODE]) == "0o100644"


class TestInstaller:

    def test_isdir_kbtogglr(self, tmpdir: fixture):
        env = environ(tmpdir)
        installer_ = prepare_obj(env, Installer)
        installer_.run_installer()
        assert path.isdir(env["kbtogglr"])

    def test_isdir_bin(self, tmpdir: fixture):
        env = environ(tmpdir)
        installer_ = prepare_obj(env, Installer)
        installer_.run_installer()
        assert path.isdir(env["bin"])

    def test_islink_exec(self, tmpdir: fixture):
        env = environ(tmpdir)
        installer_ = prepare_obj(env, Installer)
        installer_.run_installer()
        assert path.islink(env["exec"])

    def test_mode_installer(self, tmpdir: fixture):
        env = environ(tmpdir)
        installer_ = prepare_obj(env, Installer)
        installer_.run_installer()
        assert oct(stat(env["main"])[ST_MODE]) == "0o100755"


class TestUninstaller:

    def test_not_isdir_kbtogglr(self, tmpdir: fixture):
        env = environ(tmpdir)
        uninstaller_ = prepare_obj(env, Uninstaller)
        uninstaller_.run_uninstaller()
        assert not path.isdir(env["kbtogglr"])

    def test_not_islink_exec(self, tmpdir: fixture):
        env = environ(tmpdir)
        uninstaller_ = prepare_obj(env, Uninstaller)
        uninstaller_.run_uninstaller()
        assert not path.islink(env["exec"])

    def test_isfile_desktop(self, tmpdir: fixture):
        env = environ(tmpdir)
        uninstaller_ = prepare_obj(env, Uninstaller)
        uninstaller_.run_uninstaller()
        assert not path.isfile(env["desktop"])
