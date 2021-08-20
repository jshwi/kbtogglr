"""
kbtogglr
========
"""
import os as _os
import tempfile as _tempfile
from pathlib import Path as _Path
from subprocess import run as _run
from typing import List as _List
from typing import Optional as _Optional

import appdirs as _appdirs

__version__ = "1.0.0"

_IMAGES = _Path(__file__).parent / "images"
_ON = str(_IMAGES / "on.png")
_OFF = str(_IMAGES / "off.png")


class CommandNotFoundError(FileNotFoundError):
    """Raise if ``xinput`` has not been installed."""


class _Lock:
    """Create lock file to signal to program whether keyboard is on.

    Determine whether lock-file exists. If lock-file exists then read it
    for the path to the secured temp file, otherwise leave the value as
    None. If for some reason the path key does not exist continue, as
    this can be enabled later.

    This is intentionally ambiguous as `xinput` resets automatically
    after a reboot, as will the lock.

    :param lock_dir: Directory to search and add lock file.
    """

    def __init__(self, lock_dir: _Path) -> None:
        self.tempfile: _Optional[_Path] = None
        self.lock_file = lock_dir / "lock"
        if self.lock_file.is_file():
            with open(self.lock_file) as fin:
                self.tempfile = _Path(fin.read())

    def acquired(self) -> bool:
        """Determine whether lock-file exists.

        :return: Return whether lock has been acquired. True or False.
        """
        if self.tempfile is not None:
            return self.tempfile.is_file()

        return False

    def enable(self) -> None:
        """Enable lock.

        Create a new secure temp file and save the path to the lock.
        """

        with open(self.lock_file, "w") as fout:
            fout.write(_tempfile.mkstemp()[1])

    def disable(self) -> None:
        """Disable lock, if one exists."""
        if self.tempfile is not None:
            _os.remove(self.tempfile)


def _get_id(value: str, output: str) -> str:
    # take the output and str value, and parse it for keyboard id
    for line in output.splitlines():
        if value in line:

            # iterate over the keyboard data to find the ids within
            # string return id or return None if id was not found
            for split_line in line.split():
                if "id=" in split_line:

                    # if a declaration of the id has been found split
                    # the numerical id value from the rest of the string
                    return split_line.split("=")[1]

    raise RuntimeError("cannot detect keyboard id")


def _xinput_list() -> str:
    # return the output of `xinput list`
    # if `FileNotFoundError` is raised, catch it and return a more
    # user-friendly `CommandNotFoundError`
    try:
        proc = _run(["xinput", "list"], capture_output=True, check=True)
        return proc.stdout.decode()
    except FileNotFoundError as err:
        raise CommandNotFoundError("xinput: command not found...") from err


def _get_ids() -> _List[str]:
    # capture the values of `xinput list` to find keyboard ids
    # loop over slave and master keyboards, searching for matched value
    # return replaced values with keyboard ids or raise `RuntimeError`
    patterns = "AT Translated Set 2 keyboard", "Virtual core keyboard"
    output = _xinput_list()
    return [_get_id(i, output) for i in patterns]


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
    slave, master = _get_ids()
    lock = _Lock(_cache_dir())
    if lock.acquired():
        _toggle_on(slave, master)
        lock.disable()
    else:
        _toggle_off(slave)
        lock.enable()
