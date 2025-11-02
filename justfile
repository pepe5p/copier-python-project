TEST_CATALOG := "test_catalog"
DEFAULT_OUTPUT := TEST_CATALOG + "/generated_project"
DOCKER_OUTPUT := TEST_CATALOG + "/dockerized_project"
PLAIN_OUTPUT := TEST_CATALOG + "/plain_project"
PATHS_TO_LINT := "tests"

[doc("Command run when 'just' is called without any arguments")]
default: help

[doc("Prints this help message.")]
help:
	just --list

[group("generation")]
[doc("Generates repo from template to output directory")]
copy data_file output=DEFAULT_OUTPUT:
    uv run copier copy . {{ output }} \
    --vcs-ref=HEAD \
    --data-file {{ data_file }} \
    --overwrite \
    --UNSAFE \
    --force

[group("generation")]
[doc("Runs linters and tests in the output directory (docker variant).")]
output_all_ff_docker output=DEFAULT_OUTPUT:
	cp {{ output }}/.env.example {{ output }}/.env
	cd {{ output }} && uv lock
	just --justfile {{ output }}/justfile dc all_ff

[group("generation")]
[doc("Runs linters and tests in the output directory.")]
output_all_ff output=DEFAULT_OUTPUT:
	cd {{ output }} && uv lock
	just --justfile {{ output }}/justfile all_ff

[group("development")]
[doc("Run all checks and tests (lints, mypy, tests...)")]
all: lint_full test generation_check generation_check_docker

[group("development")]
[doc("Run all checks and tests, but fail on first that returns error (lints, mypy, tests...)")]
all_ff: lint_full_ff test generation_check generation_check_docker

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

[group("development")]
[group("generation")]
generation_check_docker data_file="test_answers/docker.yml" output=DOCKER_OUTPUT:
    just copy {{ data_file }} {{ output }}
    just output_all_ff_docker {{ output }}

[group("development")]
[group("generation")]
generation_check  data_file="test_answers/plain.yml" output=PLAIN_OUTPUT:
    just copy {{ data_file }} {{ output }}
    just output_all_ff {{ output }}
