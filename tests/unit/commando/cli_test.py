from importlib.metadata import version

import pytest

from commando.cli import cli


def test_it():
    cli([])


def test_help():
    with pytest.raises(SystemExit) as exc_info:
        cli(["--help"])

    assert not exc_info.value.code


def test_version(capsys):
    exit_code = cli(["--version"])

    assert capsys.readouterr().out.strip() == version("commando")
    assert not exit_code
