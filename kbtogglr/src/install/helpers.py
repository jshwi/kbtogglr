import os
from contextlib import redirect_stdout


def print_color(str_: str, bold=False) -> None:
    print(f"\u001b[{int(bold)};{33};40m{str_}\u001b[0;0m")


def suppress_stdout(func):
    def wrapper(*args, **kwargs):
        with open(os.devnull, 'w') as devnull:
            with redirect_stdout(devnull):
                func(*args, **kwargs)
    return wrapper
