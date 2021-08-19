"""
kbtogglr
========
"""
import os
import tempfile
from configparser import ConfigParser
from pathlib import Path
from subprocess import PIPE, Popen, call
from typing import Dict, List, Optional

import appdirs

__version__ = "1.0.0"

ASSETS = Path(__file__).parent / "images"


class Lock:
    """Create lock file to signal to program whether keyboard is on.

    :param lock_dir: Directory to search and add lock file.
    """

    def __init__(self, lock_dir: Path) -> None:
        self.tempfile: Optional[Path] = None
        self.lock_file = lock_dir / "lock"
        self.config = ConfigParser()

    def acquired(self) -> bool:
        """Return whether lock has been acquired.

        :return: Lock acquired? True or False.
        """
        if self.lock_file.is_file():
            self.config.read(self.lock_file)
            path = self.config["DEFAULT"].get("path")
            if path is not None:
                self.tempfile = Path(path)
                return self.tempfile.is_file()

        return False

    def enable(self) -> None:
        """Enable lock."""
        self.tempfile = Path(tempfile.mkstemp()[1])
        self.config["DEFAULT"]["path"] = str(self.tempfile)
        with open(self.lock_file, "w") as fout:
            self.config.write(fout)

    def disable(self) -> None:
        """Disable lock."""
        if self.tempfile is not None:
            os.remove(self.tempfile)


def _get_id(value: str, output: List[str]) -> str:
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


def _get_ids() -> Dict[str, str]:
    # capture the values of `xinput list` to find keyboard ids
    # loop over slave and master keyboards, searching for matched value
    # return replaced values with keyboard ids or raise `RuntimeError`
    ids = {
        "master": "Virtual core keyboard",
        "slave": "AT Translated Set 2 keyboard",
    }
    with Popen(
        ["xinput", "list"], stdout=PIPE, bufsize=1, universal_newlines=True
    ) as proc:
        output = proc.communicate()[0].splitlines()

    for key, value in ids.items():
        ids[key] = _get_id(value, output)

    return ids


def main() -> None:
    """run commands to toggle keyboard on or off.

    Arguments depend on whether keyboard is currently on or off.

    :raise RuntimeError: Raise if no keyboard ID can be parsed.
    """
    ids = _get_ids()
    cache_dir = Path(appdirs.user_cache_dir(__name__))
    cache_dir.mkdir(exist_ok=True, parents=True)
    lock = Lock(cache_dir)
    notify = ["notify-send", "-i"]
    xinput = ["xinput"]
    if lock.acquired():
        notify.extend(
            [str(ASSETS / "on.png"), "Enabling Keyboard...", "Connected"]
        )
        xinput.extend(["reattach", ids["slave"], ids["master"]])
        lock.disable()
    else:
        notify.extend(
            [str(ASSETS / "off.png"), "Disabling Keyboard...", "Disconnected"]
        )
        xinput.extend(["float", ids["slave"]])
        lock.enable()

    call(notify)
    call(xinput)
