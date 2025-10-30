PROJECT_NAME := "copier-python-project"
TEST_CATALOG := "test_catalog"
COPIER_ANSWERS_CATALOG := ".copier"
TEST_ANSWERS_FILE := COPIER_ANSWERS_CATALOG + "/.copier-answers." + PROJECT_NAME + ".yml"
PATHS_TO_LINT := "tests"

[doc("Command run when 'just' is called without any arguments")]
default: help

[doc("Prints this help message.")]
help:
	just --list

[group("generation")]
[doc("Generates repo from template to output directory")]
copy output=TEST_CATALOG data_file="example-answers.yml":
    uv run copier copy . {{ output }} \
    --vcs-ref=HEAD \
    --data-file {{ data_file }} \
    --overwrite \
    --UNSAFE \
    --force

[group("generation")]
[doc("Deletes the output directory, excluding the answers file (it is remained for re-copying).")]
clear output=TEST_CATALOG:
	find "{{ output }}" -mindepth 1 \
	-not -path "{{ output }}/{{ COPIER_ANSWERS_CATALOG }}" \
	-not -path "{{ output }}/{{ TEST_ANSWERS_FILE }}" \
	-delete

[group("generation")]
[doc("Re-copies the template to the output directory, using the answers file. If clear is true, it deletes the output directory first.")]
recopy output=TEST_CATALOG clear="true" skip-answered="true":
	@if {{ clear }}; then \
		just clear {{ output }}; \
	fi
	uv run copier recopy {{ output }} \
	--vcs-ref=HEAD \
	--answers-file {{ TEST_ANSWERS_FILE }} \
	--overwrite \
	{{ if skip-answered == "true" { "--skip-answered" } else { "" } }}

[group("generation")]
[doc("Same as `recopy`, but with `skip-answered=false` to allow modifying answers.")]
update output=TEST_CATALOG clear="true":
	just recopy output={{ output }} clear={{ clear }} skip-answered=false recopy

[group("generation")]
[doc("Runs linters and tests in the output directory.")]
run_lints_and_tests_in_output output=TEST_CATALOG:
	cp {{ output }}/.env.example {{ output }}/.env
	cd {{ output }} && uv lock
	just --justfile {{ output }}/justfile dc all_ff

[group("development")]
[doc("Run all checks and tests (lints, mypy, tests...)")]
all: lint_full test

[group("development")]
[doc("Run all checks and tests, but fail on first that returns error (lints, mypy, tests...)")]
all_ff: lint_full_ff test

[group("development")]
[doc("Runs template tests.")]
test:
	uv run pytest tests

[group("lint")]
[doc("Run all lint checks and mypy")]
lint_full: lint mypy
alias full_lint := lint_full

[group("lint")]
[doc("Run all lint checks and mypy, but fail on first that returns error")]
lint_full_ff: lint_ff mypy
alias full_lint_ff := lint_full_ff

[group("lint")]
[doc("Run all lightweight lint checks (no mypy)")]
@lint:
	-just ruff

[group("lint")]
[doc("Run ruff lint check (code formatting)")]
ruff:
	uv run ruff check {{PATHS_TO_LINT}}
	uv run ruff format {{PATHS_TO_LINT}} --check

[group("lint")]
[doc("Run mypy check (type checking)")]
mypy:
	uv run mypy {{PATHS_TO_LINT}} --show-error-codes --show-traceback --implicit-reexport

[group("lint")]
[doc("Run all lightweight lint checks, but fail on first that returns error")]
lint_ff: ruff

[group("lint")]
[doc("Automatically fix lint problems (only reported by ruff)")]
lint_fix:
	uv run ruff check {{PATHS_TO_LINT}} --fix
	uv run ruff format {{PATHS_TO_LINT}}

_ci_generation_check output=TEST_CATALOG:
    just copy {{ output }}
    just run_lints_and_tests_in_output {{ output }}
