#!/usr/bin/env python3
from os import path, PathLike, makedirs
from pathlib import Path
from shutil import copytree
from typing import Dict
from typing import Union

from pytest import fixture

from src.paths import ENV

path_type = Union[bytes, str, PathLike]
path_dict = Dict[str, path_type]


def prepare_obj(env: path_dict, obj):
    set_env(env)
    instance = obj()
    instance.env = env
    return instance


def make_dst(dst: path_type) -> None:
    if not path.isdir(dst):
        makedirs(dst)


def cp_repo(repo: path_type, tmp_kbhome: path_type) -> None:
    if not path.isdir(tmp_kbhome):
        copytree(repo, tmp_kbhome)


def is_tmp(path_: path_type) -> bool:
    check = Path(path_)
    part_tuple = check.parts[1:2]
    part = part_tuple[0]
    if part == "tmp":
        return True
    return False


def exclude(
        tmpdir: fixture, env: path_dict, attr: str, path_: path_type
) -> path_dict:
    if not is_tmp(path_) and attr not in ("repo", "home"):
        new_path = f"{str(tmpdir)}{path_}"
        env[attr] = new_path
    return env


def mkdirs_tmp(tmpdir: fixture, env: path_dict) -> path_dict:
    for attr in env:
        path_ = env[attr]
        env = exclude(tmpdir, env, attr, path_)
    return env


def environ(tmpdir):
    session_env = mkdirs_tmp(tmpdir, ENV)
    return session_env


def set_env(env: path_dict) -> None:
    cp_repo(str(env["repo"]), str(env["kbhome"]))
    make_dst(env["applications"])
