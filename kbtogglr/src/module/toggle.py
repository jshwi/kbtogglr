#!/usr/bin/ENV python3
"""Toggle keyboard on or off with IDs passed as dictionary parameters"""
from configparser import ConfigParser
from os import path
from subprocess import call
from typing import Dict, Union, Optional

from src.module.keyboard import Keyboard
from src.paths import ENV


class Toggle(Keyboard):
    """Toggle keyboard on and off"""

    def __init__(self) -> None:
        super().__init__()
        self.config = ConfigParser()
        self.env = ENV

    def _save_status(self, enabled: bool) -> None:
        # Save boolean value (on / off) in `.keyboard` dotfile in $HOME
        self.config["DEFAULT"] = {"enabled": enabled}
        with open(self.env["save_file"], "w") as file:
            self.config.write(file)

    def _parse_status(self) -> str:
        # if no dotfile exists already then the script assumes this
        # hasn't been run before and sets `enabled` in to True in new
        # file
        # if a file exists then the value which has been written into it
        # will be loaded into runtime
        # return True or False
        if not path.isfile(self.env["save_file"]):
            self._save_status(True)
        else:
            self.config.read(self.env["save_file"])
        return self.config.getboolean("DEFAULT", "enabled")

    def get_args(
            self, ids: Dict[str, Optional[str]] = None
    ) -> Dict[str, Union[str, bool]]:
        """return a specific dictionary of command line arguments
        depending on whether keyboard is currently on or off

        :param ids: Dictionary with `master` and `slave` IDs
        """
        status = self._parse_status()
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
        icon_path = path.join(self.env["images"], f"{icon}.png")
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
        self._save_status(cmd["status"])
