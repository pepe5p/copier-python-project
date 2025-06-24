from typing import Mapping
from pathlib import Path
from copier.cli import CopierApp

HERE = Path(__file__).parent
ROOT_DIR = HERE.parent


def generate_project(dst: Path, answers: Mapping[str, str]):
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
