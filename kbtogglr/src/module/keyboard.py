#!/usr/bin/env python3
"""Get master and slave id for laptop keyboard"""
from subprocess import Popen, PIPE
from typing import Optional, Union, List, Dict


class Keyboard:
    """
    As this value tends to change this helps user avoid the trouble of
    having to look these id values up every time they simply want to
    toggle the keyboard on or off
    """

    def __init__(self) -> None:
        self.master = "Virtual core keyboard"
        self.slave = "AT Translated Set 2 keyboard"

    @staticmethod
    def __xinput_list() -> Popen:
        # run `xinput list` with Popen() and catch stdout
        return Popen(
            "xinput list",
            shell=True,
            stdout=PIPE,
            bufsize=1,
            universal_newlines=True
        )

    @staticmethod
    def __get_device_data(
            xinput_list: Popen, name_: str
    ) -> Optional[Union[List[str], List[bytes]]]:
        # loop over slave and master keyboards
        # capture the values of `xinput list` to find keyboard ids
        # return id or return None if id was not found
        with xinput_list as output:
            for line in output.stdout:
                if name_ in line:
                    return line.split()
        return None

    @staticmethod
    def __parse_xinput_device(
            items: Optional[Union[List[str], List[bytes]]]
    ) -> Optional[Union[List[str], List[bytes]]]:
        # iterate over the keyboard data to find the ids within string
        # return id or return None if id was not found
        if items:
            for item in items:
                if "id=" in item:
                    return item.split("=")
        return None

    @staticmethod
    # if a declaration of the id has been found split the numerical id
    # value from the rest of the string
    # return id or return None if id was not found
    def __parse_id(
            items: Optional[Union[List[str], List[bytes]]]
    ) -> Optional[str]:
        if items:
            for item in items:
                if item.isdigit():
                    return item
        return None

    def catch_xinput(self, name: str) -> Optional[str]:
        """Run `xinput list` with Popen and capture stdout

        Parse stdout for keyboard device data

        Parse device data for id data

        Capture numerical id data

        Return ID or return None if id was not found

        :param name:    Name of the keyboard device
        :return:        Keyboard ID
        :raises:        RuntimeError:   ID could not be found and
                                        program cannot continue to run
        """
        xinput_list = self.__xinput_list()
        items = self.__get_device_data(xinput_list, name)
        items = self.__parse_xinput_device(items)
        id_ = self.__parse_id(items)
        if id_:
            return id_
        raise RuntimeError("cannot detect keyboard id")

    def get_ids(self) -> Dict[str, Optional[str]]:
        """Iterate over dictionary containing names of keyboard data
        which is needed

        Return IDs and not the device name

        :return:    Dictionary containing `master` or `slave` as the key
                    and the device ID as the value
        """
        ids = {}
        for key, value in self.__dict__.items():
            id_ = self.catch_xinput(value)
            ids[key] = id_
        return ids
