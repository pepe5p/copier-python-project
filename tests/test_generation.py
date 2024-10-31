import mimetypes
from pathlib import Path

from .helpers import generate_project

JINJA_LEFTOVERS = ["{%", "{#", "%}", "#}"]

TEST_ANSWERS = {
    "project_name": "test-project",
    "description": "A test project",
    "authors": "Test Test <test@test.test>",
}


def test_project_generates_without_error(tmp_path: Path) -> None:
    run_result = generate_project(dst=tmp_path, answers=TEST_ANSWERS)
    assert run_result[1] == 0


def test_no_leftovers(tmp_path: Path) -> None:
    generate_project(dst=tmp_path, answers=TEST_ANSWERS)
    
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
                
    assert not files_with_leftovers, f"Files that contains jinja leftovers: {files_with_leftovers}"
