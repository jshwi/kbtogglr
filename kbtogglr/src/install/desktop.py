from configparser import ConfigParser
from os import path, chmod

from src.install.helpers import print_color
from src.paths import ENV


class Desktop:
    """Configure environment specific attributes for `.desktop_` file"""

    def __init__(self) -> None:
        self.config = ConfigParser()
        self.env = ENV

    def __configure_config(self) -> None:
        self.config.optionxform = str

    def __read_template(self) -> None:
        self.config.read(self.env["template"])

    def __configure_exec(self) -> None:
        print_color("  - Configuring executable path:")
        print(f"    Exec = \"{self.env['exec']}\"")
        self.config["Desktop Entry"]["Exec"] = self.env["exec"]

    def __configure_icon(self) -> None:
        print_color("  - Configuring icon location:")
        icon = path.join(self.env["home_static"], "icon.png")
        print(f"    Icon = \"{icon}\"")
        self.config["Desktop Entry"]["Icon"] = icon

    def __write_desktop_file(self) -> None:
        print_color(f"  - Writing `kbtogglr.desktop`:")
        print(f"    {self.env['template']} -> {self.env['desktop']}")
        with open(self.env["desktop"], "w") as file:
            self.config.write(file, space_around_delimiters=False)

    def __change_app_mode(self) -> None:
        chmod(self.env["desktop"], 0o644)

    def write_launcher(self) -> None:
        """Write launcher data to file and then run chmod 644 on it"""
        self.__write_desktop_file()
        self.__change_app_mode()

    def run_desktop(self) -> None:
        """Run methods that will configure and install an application
        launcher for use with gui
        """
        self.__configure_config()
        self.__read_template()
        self.__configure_exec()
        self.__configure_icon()
        self.write_launcher()
