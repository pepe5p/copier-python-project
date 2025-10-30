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

### Prerequisites

1. Install python 3.13 or greater. Consider using [pyenv](https://github.com/pyenv/pyenv#installation) if you work with multiple python versions
2. Install [uv](https://github.com/astral-sh/uv#installation)
3. Install project dependencies: `uv sync --dev`

### Running tests

1. run `uv run pytest` in your root directory

### Running template locally

1. copier cli: `copier copy . test-folder-path`
