from pathlib import Path
from typing import Any

import pytest


@pytest.fixture()
def answers() -> dict[str, Any]:
    """Fixture to provide default answers for project generation."""
    return {
        "author_name": "test-author",
        "author_email": "author@email.test",
        "project_name": "test-project",
        "docker": True,
        "description": "A test project",
    }


def determine_file_type(path: Path) -> str:
    if not path.suffix:
        return path.name

    suffixes = path.suffixes

    if len(suffixes) == 1:
        if suffixes[0] == ".example":
            return path.stem

        return path.suffix

    if suffixes[-1] == ".example":
        return suffixes[-2]

    return suffixes[-1]
