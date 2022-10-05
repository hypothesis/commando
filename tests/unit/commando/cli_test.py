from importlib.metadata import version

import pytest

from commando.cli import cli


def test_defaults(commando):
    cli(
        [
            "--repos",
            "hypothesis/repo-1",
            "hypothesis/repo-2",
            "hypothesis/repo-3",
            "--branch",
            "my_branch",
            "--command",
            "my_command",
        ]
    )

    commando.assert_called_once_with(
        ["hypothesis/repo-1", "hypothesis/repo-2", "hypothesis/repo-3"],
        "my_command",
        "Automated changes by Commando",
        "my_branch",
        "Automated changes by Commando",
        "Automated changes by [Commando](https://github.com/hypothesis/commando)",
    )


def test_options(commando):
    cli(
        [
            "--repos",
            "hypothesis/repo-1",
            "hypothesis/repo-2",
            "hypothesis/repo-3",
            "--branch",
            "my_branch",
            "--command",
            "my_command",
            "--commit-message",
            "my_commit_message",
            "--pr-title",
            "my_pr_title",
            "--pr-body",
            "my_pr_body",
        ]
    )

    commando.assert_called_once_with(
        ["hypothesis/repo-1", "hypothesis/repo-2", "hypothesis/repo-3"],
        "my_command",
        "my_commit_message",
        "my_branch",
        "my_pr_title",
        "my_pr_body",
    )


def test_help():
    with pytest.raises(SystemExit) as exc_info:
        cli(["--help"])

    assert not exc_info.value.code


def test_version(capsys):
    with pytest.raises(SystemExit) as exc_info:
        cli(["--version"])

    assert capsys.readouterr().out.strip() == version("commando")
    assert not exc_info.value.code


@pytest.fixture(autouse=True)
def commando(mocker):
    return mocker.patch("commando.cli.commando", autospec=True)
