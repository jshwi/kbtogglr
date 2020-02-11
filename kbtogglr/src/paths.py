#!/usr/bin/env python3
from os import path, PathLike
from typing import Dict, Union


def environment() -> Dict[str, Union[bytes, str, PathLike]]:
    """Paths and files for installing package

    :return: Dictionary for desktop/installer/uninstaller classes
    """
    # absolute
    # # dirs
    home = path.expanduser("~")
    local = path.join(home, ".local")
    share = path.join(local, "share")
    bin_ = path.join(local, "bin")
    applications = path.join(share, "applications")
    kbhome = path.join(home, ".kbtogglr")
    home_docs = path.join(kbhome, "docs")
    home_static = path.join(home_docs, "_static")
    kbpackage = path.join(kbhome, "kbtogglr")
    lib = path.join(kbpackage, "lib")
    tmp = path.join("/tmp")
    # # files
    exec_ = path.join(bin_, "kbtogglr")
    desktop = path.join(applications, "kbtogglr.desktop")
    main = path.join(kbpackage, "__main__.py")
    template = path.join(lib, "template.desktop")
    save_file = path.join(tmp, "kbstatus")
    # relative
    # # dirs (no files)
    src = path.dirname(path.realpath(__file__))
    package = path.dirname(src)
    repo = path.dirname(package)
    docs = path.join(repo, "docs")
    images = path.join(docs, "_static")

    # paths that are not just constructors but are used to install
    # package too
    return {
        "bin": bin_,
        "kbtogglr": kbhome,
        "repo": repo,
        "package": package,
        "applications": applications,
        "save_file": save_file,
        "images": images,
        "desktop": desktop,
        "exec": exec_,
        "main": main,
        "template": template,
        "kbhome": kbhome,
        "home_static": home_static
    }


# variable to import
ENV = environment()
