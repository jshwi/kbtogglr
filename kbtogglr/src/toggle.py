#!/usr/bin/env python3
"""Toggle keyboard on or off with IDs passed as dictionary parameters"""
from configparser import ConfigParser
from os import path
from subprocess import call
from typing import Dict, Union, Optional

from src.keyboard import Keyboard


class Toggle(Keyboard):
    """Toggle keyboard on and off"""

    def __init__(self) -> None:
        super().__init__()
        self.config = ConfigParser()
        self.src = path.dirname(path.realpath(__file__))
        self.package = path.dirname(self.src)
        self.repo = path.dirname(self.package)
        self.home = path.expanduser("~")
        self.save_file = path.join(self.home, ".kbstatus")
        self.images = path.join(self.repo, "docs", "_static")

    def __save_status(self, enabled: bool) -> None:
        # Save boolean value (on / off) in `.keyboard` dotfile in $HOME
        self.config["DEFAULT"] = {"enabled": enabled}
        with open(self.save_file, "w") as file:
            self.config.write(file)

    def __parse_status(self) -> str:
        # if no dotfile exists already then the script assumes this
        # hasn't been run before and sets `enabled` in to True in new
        # file
        # if a file exists then the value which has been written into it
        # will be loaded into runtime
        # return True or False
        if not path.isfile(self.save_file):
            self.__save_status(True)
        else:
            self.config.read(self.save_file)
        return self.config.getboolean("DEFAULT", "enabled")

    def get_args(
            self, ids: Dict[str, Optional[str]] = None
    ) -> Dict[str, Union[str, bool]]:
        """return a specific dictionary of command line arguments
        depending on whether keyboard is currently on or off

        :param ids: Dictionary with `master` and `slave` IDs
        """
        status = self.__parse_status()
        if status:
            stat = False
            icon = "off"
            action = "Disabling"
            result = "Disconnected"
            xargs = f"float {ids['slave']}"
        else:
            stat = True
            icon = "on"
            action = "Enabling"
            result = "Connected"
            xargs = f"reattach {ids['slave']} {ids['master']}"
        icon_path = path.join(self.images, f"{icon}.png")
        notice = f'"{action} Keyboard..." \\ "{result}";'
        return {
            "status": stat,
            "notify": f'notify-send -i {icon_path} {notice}',
            "xinput": f"xinput {xargs}"
        }

    def run(self, cmd: Dict[str, Union[str, bool]]) -> None:
        """run commands to toggle keyboard on or off"""
        call(cmd["notify"], shell=True)
        call(cmd["xinput"], shell=True)
        self.__save_status(cmd["status"])
