from enum import Enum, StrEnum
from pathlib import Path
from typing import Any, Final

import pytest
from _pytest.fixtures import FixtureRequest


class ProjectType(StrEnum):
    EMPTY = "empty"
    DOCKERIZED = "dockerized"
    AWS_LAMBDA = "lambda"


DEFAULT_ANSWERS = {
    "author_email": "author@email.test",
    "author_name": "test-author",
    "automatic_gh_release": True,
    "enforce_conventional_commits": True,
    "description": "A test project",
    "project_name": "test-project",
    "project_type": "dockerized",
    "specify_author": True,
}


class ArgSetType(Enum):
    NOTSET = 0
    DEFAULT = 1


NOTSET: Final = ArgSetType.NOTSET
DEFAULT: Final = ArgSetType.DEFAULT


def create_answers(
    author_email: str | ArgSetType = DEFAULT,
    author_name: str | ArgSetType = DEFAULT,
    automatic_gh_release: bool | ArgSetType = DEFAULT,
    description: str | ArgSetType = DEFAULT,
    enforce_conventional_commits: bool | ArgSetType = DEFAULT,
    project_name: str | ArgSetType = DEFAULT,
    project_type: ProjectType | ArgSetType = DEFAULT,
    specify_author: bool | ArgSetType = DEFAULT,
) -> dict[str, Any]:
    """
    Fixture to easily create different answer sets for tests.
    Each argument can be set to:
    - A specific value
    - DEFAULT to use the default answer
    - NOTSET to omit the answer (useful for testing optional questions)
    """
    return {
        key: DEFAULT_ANSWERS[key] if value is DEFAULT else value
        for key, value in {
            "author_email": author_email,
            "author_name": author_name,
            "automatic_gh_release": automatic_gh_release,
            "description": description,
            "enforce_conventional_commits": enforce_conventional_commits,
            "project_name": project_name,
            "project_type": project_type,
            "specify_author": specify_author,
        }.items()
        if value is not NOTSET
    }


@pytest.fixture(
    params=[
        pytest.param(create_answers(project_type=ProjectType.AWS_LAMBDA), id="lambda"),
        pytest.param(create_answers(project_type=ProjectType.DOCKERIZED), id="dockerized"),
        pytest.param(create_answers(project_type=ProjectType.EMPTY), id="plain"),
        pytest.param(
            create_answers(specify_author=False, author_name=NOTSET, author_email=NOTSET),
            id="no-author",
        ),
        pytest.param(
            create_answers(enforce_conventional_commits=False, automatic_gh_release=NOTSET),
            id="no-cc-no-release",
        ),
    ],
)
def answers(
    request: FixtureRequest,
) -> dict[str, Any]:
    return request.param


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
