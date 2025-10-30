from pathlib import Path
from typing import Mapping, Union

from copier.cli import CopierApp

StrOrPath = Union[str, Path]

HERE = Path(__file__).parent
ROOT_DIR = HERE.parent


def generate_project(dst: Path, answers: Mapping[str, str]) -> tuple[CopierApp, int]:
    """Generate copier project with test-friendly defaults."""
    return CopierApp.run(
        [
            "copier",
            "copy",
            "--vcs-ref=HEAD",  # IMPORTANT!  needed to use the latest changes on the file system
            *[f"--data={k}={v}" for k, v in answers.items()],
            str(ROOT_DIR),
            str(dst),
            "--quiet",
            "--defaults",
        ],
        exit=False,
    )


def is_in_file(file: Path, *args: str) -> bool:
    with open(file, "r") as f:
        content = f.read()
        return all(arg in content for arg in args)
