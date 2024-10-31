# copier-python-project

## Usage

1. [Install copier](https://github.com/copier-org/copier#installation)
2. Generate a new project or apply this template to an existing project:
    ```bash
    PROJECT_PATH=my-project # relative path including project dir name, will be created automatically if it not exist.
    copier copy gh:pepe5p/copier-python-project $PROJECT_PATH
    ```
   or just:
    ```bash
    copier copy gh:pepe5p/copier-python-project .
    ```

## Development

Familiarize yourself with the [copier templating engine](https://copier.readthedocs.io/en/stable/)

> [!NOTE]
> If file not ends on `.jinja`, it will be copy-pasted as is.
> When you add `.jinja` - make sure that there will no conflicts between template languages, or just wrap everything not related to copier templating in `{%raw%}` `{%endraw%}`

### Prerequisities

1. Install python 3.11 or greater. Consider using [pyenv](https://github.com/pyenv/pyenv#installation) if you work with multiple python versions
2. Install [poetry](https://python-poetry.org/docs/#installation)
3. configure poetry to use a local virtualenv: `poetry config virtualenvs.in-project true`
4. Install project dependencies: `poetry install`

### Running tests

1. activate virtualenv: `source .venv/bin/activate`
2. run `pytest` in your root directory

### Running template localy

1. copier cli: `copier copy . test-folder-path`
