import mimetypes
from enum import StrEnum
from pathlib import Path

import pytest

from .conftest import determine_file_type
from .helpers import generate_project
from .parsers import PARSERS

JINJA_LEFTOVERS = ["{%", "{#", "%}", "#}"]


class ProjectType(StrEnum):
    EMPTY = "empty"
    DOCKERIZED = "dockerized"
    AWS_LAMBDA = "lambda"


ALL_PROJECT_TYPES = list(ProjectType)


@pytest.mark.parametrize("project_type", ALL_PROJECT_TYPES)
def test_no_leftovers(
    project_type: ProjectType,
    tmp_path: Path,
    answers: dict,
) -> None:
    answers["project_type"] = project_type

    run_result = generate_project(tmp_path, answers)

    assert run_result[1] == 0

    files_with_leftovers = []
    for file in tmp_path.rglob("*"):
        if not file.is_file():
            continue

        mime_type, _ = mimetypes.guess_type(file)
        if mime_type is not None and mime_type.startswith("image"):
            continue

        with open(file, "r", encoding="utf-8") as f:
            content = f.read()
            if any(leftover in content for leftover in JINJA_LEFTOVERS):
                relative_file = file.relative_to(tmp_path)
                files_with_leftovers.append(relative_file.as_posix())

    assert not files_with_leftovers, f"Files that contain jinja leftovers: {files_with_leftovers}"


@pytest.mark.parametrize(
    ("filename", "expected"),
    [
        ("script.py", ".py"),
        ("config.yaml", ".yaml"),
        ("config.yml", ".yml"),
        ("settings.toml", ".toml"),
        ("Dockerfile.example", "Dockerfile"),
        (".env.example", ".env"),
        ("script.py.mako", ".mako"),
        ("Dockerfile", "Dockerfile"),
        ("justfile", "justfile"),
        ("docker-compose.override.yml.example", ".yml"),
    ],
)
def test_determine_file_type(filename: str, expected: str) -> None:
    assert determine_file_type(path=Path(filename)) == expected


@pytest.mark.parametrize("project_type", ALL_PROJECT_TYPES)
def test_files_syntax(
    project_type: ProjectType,
    tmp_path: Path,
    answers: dict,
) -> None:
    answers["project_type"] = project_type

    run_result = generate_project(tmp_path, answers)

    assert run_result[1] == 0

    skipped_files = 0
    checked_files = 0

    for file in tmp_path.rglob("*"):
        if not file.is_file():
            continue

        file_type = determine_file_type(path=file)
        if file_type is None:
            skipped_files += 1
            continue

        parser = PARSERS.get(file_type)
        if parser is None:
            skipped_files += 1
            continue

        with open(file, "r", encoding="utf-8") as f:
            content = f.read()
            try:
                parser(content=content)
                checked_files += 1
            except Exception as e:
                pytest.fail(f"Failed to parse {file.relative_to(tmp_path)}: {e}")

    assert checked_files != 0, f"No files were checked, skipped {skipped_files} files."
