import tomllib
from pathlib import Path

import pymind

PYPROJECT = Path(__file__).resolve().parent.parent / "pyproject.toml"


def test_version_matches_pyproject() -> None:
    with PYPROJECT.open("rb") as f:
        expected = tomllib.load(f)["project"]["version"]

    assert pymind.__version__ == expected
