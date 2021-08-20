"""
kbtogglr
========
"""
import os as _os
import tempfile as _tempfile
from configparser import ConfigParser as _ConfigParser
from pathlib import Path as _Path
from subprocess import run as _run
from typing import Dict as _Dict
from typing import List as _List
from typing import Optional as _Optional

import appdirs as _appdirs

__version__ = "1.0.0"

_IMAGES = _Path(__file__).parent / "images"
_ON = str(_IMAGES / "on.png")
_OFF = str(_IMAGES / "off.png")


class _Lock:
    """Create lock file to signal to program whether keyboard is on.

    :param lock_dir: Directory to search and add lock file.
    """

    def __init__(self, lock_dir: _Path) -> None:
        self.tempfile: _Optional[_Path] = None
        self.lock_file = lock_dir / "lock"
        self.config = _ConfigParser()

    def acquired(self) -> bool:
        """Return whether lock has been acquired.

        :return: Lock acquired? True or False.
        """
        if self.lock_file.is_file():
            self.config.read(self.lock_file)
            path = self.config["DEFAULT"].get("path")
            if path is not None:
                self.tempfile = _Path(path)
                return self.tempfile.is_file()

        return False

    def enable(self) -> None:
        """Enable lock."""
        self.tempfile = _Path(_tempfile.mkstemp()[1])
        self.config["DEFAULT"]["path"] = str(self.tempfile)
        with open(self.lock_file, "w") as fout:
            self.config.write(fout)

    def disable(self) -> None:
        """Disable lock."""
        if self.tempfile is not None:
            _os.remove(self.tempfile)


def _get_id(value: str, output: _List[str]) -> str:
    # take the output and str value, and parse it for keyboard id
    for line in output:
        if value in line:

            # iterate over the keyboard data to find the ids within
            # string return id or return None if id was not found
            for split_line in line.split():
                if "id=" in split_line:

                    # if a declaration of the id has been found split
                    # the numerical id value from the rest of the string
                    return split_line.split("=")[1]

    raise RuntimeError("cannot detect keyboard id")


def _get_ids() -> _Dict[str, str]:
    # capture the values of `xinput list` to find keyboard ids
    # loop over slave and master keyboards, searching for matched value
    # return replaced values with keyboard ids or raise `RuntimeError`
    ids = {
        "master": "Virtual core keyboard",
        "slave": "AT Translated Set 2 keyboard",
    }
    proc = _run(["xinput", "list"], capture_output=True, check=True)
    output = proc.stdout.decode()
    for key, value in ids.items():
        ids[key] = _get_id(value, output.splitlines())

    return ids


def _cache_dir() -> _Path:
    # create and return cache dir
    cache_dir = _Path(_appdirs.user_cache_dir(__name__))
    cache_dir.mkdir(exist_ok=True, parents=True)
    return cache_dir


def _toggle_on(slave: str, master: str) -> None:
    # run `xinput` to reattach the slave and master keyboard ids
    # send notification, including on image
    _run(["xinput", "reattach", slave, master], check=True)
    _run(
        ["notify-send", "-i", _ON, "Enabling Keyboard...", "Connected"],
        check=True,
    )


def _toggle_off(slave: str) -> None:
    # run `xinput` to detach the slave device
    # send notification, including off image
    _run(["xinput", "float", slave], check=True)
    _run(
        ["notify-send", "-i", _OFF, "Disabling Keyboard...", "Disconnected"],
        check=True,
    )


def main() -> None:
    """run commands to toggle keyboard on or off.

    Arguments depend on whether keyboard is currently on or off.

    :raise RuntimeError: Raise if no keyboard ID can be parsed.
    """
    ids = _get_ids()
    lock = _Lock(_cache_dir())
    if lock.acquired():
        _toggle_on(ids["slave"], ids["master"])
        lock.disable()
    else:
        _toggle_off(ids["slave"])
        lock.enable()
