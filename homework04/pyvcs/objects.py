import hashlib
import os
import pathlib
import re
import stat
import typing as tp
import zlib

from pyvcs.refs import update_ref
from pyvcs.repo import repo_find


def hash_object(data: bytes, fmt: str, write: bool = False) -> str:
    fmt_data = (fmt + " " + str(len(data))).encode() + b"\00" + data
    sha1 = hashlib.sha1(fmt_data).hexdigest()
    if write:
        gitdir = repo_find()
        (gitdir / "objects" / sha1[:2]).mkdir(exist_ok=True)
        with (gitdir / "objects" / sha1[:2] / sha1[2:]).open("wb") as f:
            f.write(zlib.compress(fmt_data))
    return sha1


def resolve_object(obj_name: str, gitdir: pathlib.Path) -> tp.List[str]:
    content = []
    danger = Exception(f"Not a valid object name {obj_name}")
    if len(obj_name) > 40 or len(obj_name) < 4:
        raise danger
    for file in (gitdir / "objects" / obj_name[:2]).glob(f"{obj_name[2:]}*"):
        content.append(obj_name[:2] + file.name)
    if len(content) == 0:
        raise danger
    return content


def find_object(obj_name: str, gitdir: pathlib.Path) -> str:
    pass


def read_object(sha: str, gitdir: pathlib.Path) -> tp.Tuple[str, bytes]:
    path = gitdir / "objects" / sha[:2] / sha[2:]
    with open(path, "rb") as f:
        data = zlib.decompress(f.read())
    return data.split(b" ")[0].decode(), data.split(b"\00", maxsplit=1)[1]


def read_tree(data: bytes) -> tp.List[tp.Tuple[int, str, str]]:
    tree = []
    while data:
        sha_pos = data.index(b"\00")
        mode, name = map(lambda x: x.decode(), data[:sha_pos].split(b" "))
        sha = data[sha_pos + 1 : sha_pos + 21]
        tree.append((int(mode), str(sha.hex()), str(name)))
        data = data[sha_pos + 21 :]
    return tree


def cat_file(obj_name: str, pretty: bool = True) -> None:
    fmt, data = read_object(obj_name, repo_find())
    if fmt in ["blob", "commit"]:
        print(data.decode())
    else:
        for index in read_tree(data):
            print(
                f"{index[0]:06}",
                "tree" if index[0] == 40000 else "blob",
                index[1] + "\t" + index[2],
            )


def find_tree_files(tree_sha: str, gitdir: pathlib.Path) -> tp.List[tp.Tuple[str, str]]:
    pass


def commit_parse(raw: bytes, start: int = 0, dct=None):
    content: tp.Dict[str, tp.Any]
    content = {"message": []}
    for line in raw.decode().split("\n"):
        if line.startswith(("tree", "parent", "author", "committer")):
            name, val = line.split(" ", maxsplit=1)
            content[name] = val
        else:
            content["message"].append(line)
    return content