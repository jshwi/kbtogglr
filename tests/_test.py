#!/usr/bin/env python3
from os import path, stat
from stat import ST_MODE


class TestDesktop:
    
    def test_isfile_desktop(self, desktop_, run_desktop):
        assert path.isfile(desktop_.desktop)

    def test_mode_desktop(self, desktop_, run_desktop):
        assert oct(stat(desktop_.desktop)[ST_MODE]) == "0o100644"


class TestInstaller:

    def test_isdir_kbtogglr(self, installer_, run_installer):
        assert path.isdir(installer_.kbtogglr)

    def test_isdir_bin(self, installer_, run_installer):
        assert path.isdir(installer_.bin)

    def test_islink_exec(self, installer_, run_installer):
        assert path.islink(installer_.exec)

    def test_mode_installer(self, installer_, run_desktop):
        assert oct(stat(installer_.main)[ST_MODE]) == "0o100755"

    def test_desktop(self, desktop_, run_desktop):
        TestDesktop().test_isfile_desktop(desktop_, run_desktop)
        TestDesktop().test_mode_desktop(desktop_, run_desktop)


class TestUninstaller:

    def test_not_isdir_kbtogglr(
            self, uninstaller_, run_installer, run_uninstaller
    ):
        assert not path.isdir(uninstaller_.kbtogglr)

    def test_not_islink_exec(
            self, uninstaller_, run_installer, run_uninstaller
    ):
        assert not path.islink(uninstaller_.exec)

    def test_isfile_desktop(self, desktop_, run_desktop, run_uninstaller):
        assert not path.isfile(desktop_.desktop)

