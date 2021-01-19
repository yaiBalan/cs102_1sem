import os
import pathlib
import typing as tp


def repo_find(workdir: tp.Union[str, pathlib.Path] = ".") -> pathlib.Path:
    gitdir = os.getenv("GIT_DIR", ".pyvcs")
    workdir = pathlib.Path(workdir)
    while pathlib.Path("/") != workdir.absolute():
        if (workdir / gitdir).is_dir():
            return workdir / gitdir
        workdir = workdir.parent
    if (workdir / gitdir).is_dir():
        return workdir / gitdir
    else:
        raise Exception("Not a git repository")


def repo_create(workdir: tp.Union[str, pathlib.Path]) -> pathlib.Path:
    gitdir = os.getenv("GIT_DIR", ".pyvcs")
    workdir = pathlib.Path(workdir)
    if workdir.is_file():
        raise Exception(f"{workdir} is not a directory")
    os.makedirs(workdir / gitdir / "refs" / "heads", exist_ok=True)
    os.makedirs(workdir / gitdir / "refs" / "tags", exist_ok=True)
    (workdir / gitdir / "objects").mkdir()
    with open(workdir / gitdir / "config", "w") as f:
        f.write(
            "[core]\n\trepositoryformatversion = 0\n\tfilemode = true\n\tbare = false\n\tlogallrefupdates = false\n",
        )
    with open(workdir / gitdir / "HEAD", "w") as f:
        f.write("ref: refs/heads/master\n")
    with open(workdir / gitdir / "description", "w") as f:
        f.write("Unnamed pyvcs repository.\n")
    return workdir / gitdir