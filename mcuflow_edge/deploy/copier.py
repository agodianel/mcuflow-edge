import shutil
from pathlib import Path


def copy_file(src: Path, dst: Path, overwrite: bool = True) -> Path:
    dst.parent.mkdir(parents=True, exist_ok=True)
    if dst.exists() and not overwrite:
        return dst
    return Path(shutil.copy2(str(src), str(dst)))


def copy_tree(src: Path, dst: Path, overwrite: bool = True) -> None:
    if dst.exists():
        if overwrite:
            shutil.rmtree(dst)
        else:
            return
    shutil.copytree(str(src), str(dst))
