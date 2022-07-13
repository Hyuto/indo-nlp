import os

import tomli

import indoNLP

file_directory = os.path.dirname(__file__)


def test_version():
    with open(os.path.join(file_directory, "..", "pyproject.toml"), "rb") as reader:
        data = tomli.load(reader)
    assert data["tool"]["poetry"]["version"] == indoNLP.__version__
