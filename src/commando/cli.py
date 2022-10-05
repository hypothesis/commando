from argparse import ArgumentParser
from importlib.metadata import version

from commando.core import commando


def cli(_argv=None):
    parser = ArgumentParser(
        description="Run commands in GitHub repos and send any resulting changes as pull requests (PRs)."
    )

    parser.add_argument(
        "-v", "--version", action="version", version=version("commando")
    )
    parser.add_argument(
        "--repos",
        required=True,
        nargs="+",
        help="the list of GitHub repos to operate on in <owner>/<repo-name> format, example: hypothesis/repo-1 hypothesis/repo-2 hypothesis/repo-3",
        metavar="REPO",
    )
    parser.add_argument(
        "--command",
        required=True,
        help="the command to run in each repo, example: 'make template'",
    )
    parser.add_argument(
        "--commit-message",
        default="Automated changes by Commando",
        help="the git commit message to use when making commits, example: 'Apply updates from cookiecutter'",
        metavar="TEXT",
    )
    parser.add_argument(
        "--commit-message-file",
        help="path to a file containing the commit message to use when making commits",
        metavar="PATH",
    )
    parser.add_argument(
        "--branch",
        required=True,
        help="the branch name to use when creating PRs, example: cookiecutter",
    )
    parser.add_argument(
        "--pr-title",
        default="Automated changes by Commando",
        help="the title to use when creating PRs, example: 'Apply updates from cookiecutter'",
        metavar="TEXT",
    )
    parser.add_argument(
        "--pr-body",
        default="Automated changes by [Commando](https://github.com/hypothesis/commando)",
        help="the body text to use when creating PRs",
        metavar="TEXT",
    )
    parser.add_argument(
        "--pr-body-file",
        help="path to a file containing the body text to use when creating PRs",
        metavar="PATH",
    )

    args = parser.parse_args(_argv)

    # --commit-message-file overrides --commit-message if both are given at once.
    if args.commit_message_file is not None:  # pragma:no cover
        with open(
            args.commit_message_file, "r", encoding="utf-8"
        ) as commit_message_file:
            args.commit_message = commit_message_file.read()

    # --pr-body-file overrides --pr-body if both are given at once.
    if args.pr_body_file is not None:  # pragma:no cover
        with open(args.pr_body_file, "r", encoding="utf-8") as pr_body_file:
            args.pr_body = pr_body_file.read()

    return commando(
        args.repos,
        args.command,
        args.commit_message,
        args.branch,
        args.pr_title,
        args.pr_body,
    )
