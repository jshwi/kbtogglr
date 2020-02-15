#!/usr/bin/env python3
"""Run primarily through a `.desktop` launcher"""
from src.module.keyboard import Keyboard
from src.module.toggle import Toggle


def main():
    """Get ID for keyboard device and then toggle it on or off"""
    toggle = Toggle()
    keyboard = Keyboard()
    ids = keyboard.get_ids()
    cmd = toggle.get_args(ids)
    toggle.run(cmd)


if __name__ == '__main__':
    main()
