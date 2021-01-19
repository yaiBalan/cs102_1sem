import os
import pathlib
import stat
import time
import typing as tp

from pyvcs.index import GitIndexEntry, read_index
from pyvcs.objects import hash_object
from pyvcs.refs import get_ref, is_detached, resolve_head, update_ref


def write_tree(gitdir: pathlib.Path, index: tp.List[GitIndexEntry], dirname: str = "") -> str:
    tree_content: tp.List[tp.Tuple[int, pathlib.Path, bytes]] = []
    subtrees: tp.Dict[str, tp.List[GitIndexEntry]] = dict()
    files = [str(x) for x in (gitdir.parent / dirname).glob("*")]
    for entry in index:
        if entry.name in files:
            tree_content.append((entry.mode, (gitdir.parent / entry.name), entry.sha1))
        else:
            dname = entry.name.lstrip(dirname).split("/", 1)[0]
            if not dname in subtrees:
                subtrees[dname] = []
            subtrees[dname].append(entry)
    for name in subtrees:
        stat = (gitdir.parent / dirname / name).stat()
        tree_content.append(
            (
                0o40000,
                gitdir.parent / dirname / name,
                bytes.fromhex(
                    write_tree(
                        gitdir,
                        subtrees[name],
                        dirname + "/" + name if dirname != "" else name,
                    )
                ),
            )
        )
    tree_content.sort(key=lambda x: x[1])
    data = b"".join(
        f"{elem[0]:o} {elem[1].name}".encode() + b"\00" + elem[2] for elem in tree_content
    )
    return hash_object(data, "tree", write=True)


def commit_tree(
    gitdir: pathlib.Path,
    tree: str,
    message: str,
    parent: tp.Optional[str] = None,
    author: tp.Optional[str] = None,
) -> str:
    if author is None and "GIT_AUTHOR_NAME" in os.environ and "GIT_AUTHOR_EMAIL" in os.environ:
        author = str(
            os.getenv("GIT_AUTHOR_NAME", None)  # type: ignore
            + " "
            + f'<{os.getenv("GIT_AUTHOR_EMAIL", None)}>'  # type:ignore
        )  # type:ignore
    now = int(time.mktime(time.localtime()))
    tz = time.timezone
    if tz > 0:
        tz_str = "-"
    else:
        tz_str = "+"
    tz_str += f"{abs(tz) // 60 // 60:02}{abs(tz) // 60 % 60:02}"
    cont = [f"tree {tree}"]
    if parent is not None:
        cont.append(f"parent {parent}")
    cont.append(f"author {author} {now} {tz_str}")
    cont.append(f"committer {author} {now} {tz_str}")
    cont.append(f"\n{message}\n")
    return hash_object("\n".join(cont).encode(), "commit", write=True)