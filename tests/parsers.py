import ast
import tomllib

import yaml


def python_parser(content: str) -> None:
    ast.parse(source=content)


def yaml_parser(content: str) -> None:
    yaml.safe_load(content)


def toml_parser(content: str) -> None:
    tomllib.loads(content)


PARSERS = {
    ".py": python_parser,
    ".yaml": yaml_parser,
    ".yml": yaml_parser,
    ".toml": toml_parser,
}
