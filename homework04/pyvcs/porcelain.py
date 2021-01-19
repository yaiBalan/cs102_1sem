import os
import pathlib
import typing as tp

from pyvcs.index import read_index, update_index
from pyvcs.objects import commit_parse, find_object, find_tree_files, read_object, read_tree
from pyvcs.refs import get_ref, is_detached, resolve_head, update_ref
from pyvcs.tree import commit_tree, write_tree


def add(gitdir: pathlib.Path, paths: tp.List[pathlib.Path]) -> None:
    for path in paths:
        if path.is_dir():
            add(gitdir, list(path.glob("*")))
            return None
        update_index(gitdir, [path], write=True)


def commit(gitdir: pathlib.Path, message: str, author: tp.Optional[str] = None) -> str:
    tree = write_tree(gitdir, read_index(gitdir), str(gitdir.parent))
    parent_commit = resolve_head(gitdir)
    return str(commit_tree(gitdir, tree, message, parent_commit, author))


def checkout(gitdir: pathlib.Path, obj_name: str) -> None:
    for entry in read_index(gitdir):
        if pathlib.Path(entry.name).exists():
            os.remove(entry.name)
    commit_data = commit_parse(read_object(obj_name, gitdir)[1])
    finished = False
    while not finished:
        trees: tp.List[tp.Tuple[pathlib.Path, tp.List[tp.Tuple[int, str, str]]]] = [
            (gitdir.parent, read_tree(read_object(commit_data["tree"], gitdir)[1]))
        ]
        while trees:
            tree_path, tree_content = trees.pop()
            for file_data in tree_content:
                fmt, data = read_object(file_data[1], gitdir)
                if fmt == "tree":
                    trees.append((tree_path / file_data[2], read_tree(data)))
                    if not (tree_path / file_data[2]).exists():
                        (tree_path / file_data[2]).mkdir()
                else:
                    if not (tree_path / file_data[2]).exists():
                        with (tree_path / file_data[2]).open("wb") as f:
                            f.write(data)
                        (tree_path / file_data[2]).chmod(int(str(file_data[0]), 8))
        if "parent" in commit_data:
            commit_data = commit_parse((read_object(commit_data["parent"], gitdir)[1]))
        else:
            finished = True
    for dir in gitdir.parent.glob("*"):
        if dir != gitdir and dir.is_dir():
            try:
                os.removedirs(dir)
            except OSError:
                continue