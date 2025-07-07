PROJECT_NAME := "copier-python-project"
TEST_ANSWERS_FILE := ".copier/.copier-answers." + PROJECT_NAME + ".yml"

copy output="test_catalog":
    uv run copier copy . {{ output }} \
    --vcs-ref=HEAD

recopy output="test_catalog":
    uv run copier recopy {{ output }} \
    --vcs-ref=HEAD \
    --answers-file {{ TEST_ANSWERS_FILE }} \
    --skip-answered \
    --overwrite

update output="test_catalog":
    uv run copier recopy {{ output }} \
    --vcs-ref=HEAD \
    --answers-file {{ TEST_ANSWERS_FILE }} \
    --overwrite

all_ff output="test_catalog":
    just recopy {{ output }}
    just --justfile {{ output }}/justfile all_ff

test:
	uv run pytest tests

ci_lint_full:
	uv run copier copy . tmp/test_catalog \
	--vcs-ref=HEAD \
	--data project_name="test-project" \
	--data description="..." \
	--data author_name="Test Author" \
	--data author_email="test@test.com" \
	--data docker=false

	just --justfile tmp/test_catalog/justfile lint_full_ff
