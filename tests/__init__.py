import os
import toml
import indoNLP

file_directory = os.path.dirname(__file__)


def test_version():
    data = toml.load(os.path.join(file_directory, "..", "pyproject.toml"))
    assert data["tool"]["poetry"]["version"] == indoNLP.__version__
