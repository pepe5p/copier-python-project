PROJECT_NAME := "copier-python-project"

copy output="test_folder":
    uv run copier copy . {{ output }} \
    --vcs-ref=HEAD

recopy output="test_folder":
    uv run copier recopy {{ output }} \
    --vcs-ref=HEAD \
    --answers-file .copier/.copier-answers.{{ PROJECT_NAME }}.yml \
    --skip-answered \
    --overwrite

all_ff output="test_folder":
    just recopy {{ output }}
    just all_ff --justfile {{ output }}/justfile

test:
	uv run pytest
