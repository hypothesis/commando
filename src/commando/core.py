import subprocess
import tempfile
from functools import partial
from subprocess import PIPE, STDOUT, CalledProcessError


def _pprint(repo, message):
    print(f"{repo}> {message}")


def _run(cwd, results, command, **kwargs):
    result = subprocess.run(  # pylint:disable=subprocess-run-check
        command, cwd=cwd, stdout=PIPE, stderr=STDOUT, text=True, **kwargs
    )
    results.append(result)
    result.check_returncode()
    return result


def _process_repo(
    repo, command, commit_message, branch, pr_title, pr_body
):  # pylint:disable=too-many-arguments,too-many-positional-arguments
    # Collect the results of all commands run for this repo.
    results = []

    pprint = partial(_pprint, repo)

    with tempfile.TemporaryDirectory() as tmpdirname:
        run = partial(_run, tmpdirname, results)

        try:
            pprint("Cloning repo")
            run(
                [
                    "gh",
                    "repo",
                    "clone",
                    repo,
                    tmpdirname,
                    "--",
                    # Ensure that the origin remote is named 'origin', the
                    # default name could be overridden by the git config.
                    "--origin",
                    "origin",
                    # Try to speed it up by not cloning tags since we don't need them.
                    # Note that I don't think we can speed this up even more by
                    # using a shallow clone: gh-pr-upsert needs the commits and
                    # history in order to compare branches.
                    "--no-tags",
                ]
            )

            pprint("Creating branch")
            run(
                [
                    "git",
                    "switch",
                    # Don't automatically set upstream configuration if there's
                    # a remote tracking branch with the same name.
                    "--no-guess",
                    # Don't set upstream tracking configuration.
                    "--no-track",
                    # Create a new branch or reset an existing one to origin/main.
                    "--force-create",
                    branch,
                    "origin/main",
                ]
            )

            pprint("Running command")
            pprint(command)
            run(command, shell=True)

            pprint("Committing any changes")
            run(["git", "add", "--all"])
            run(
                [
                    "git",
                    "commit",
                    # Don't crash if there are no changes to commit.
                    # If an empty commit is created gh-pr-upsert will do the
                    # right thing and not create an empty PR.
                    "--allow-empty",
                    "--message",
                    commit_message,
                ]
            )

            pprint("Sending PR")
            try:
                result = run(["gh-pr-upsert", "--title", pr_title, "--body", pr_body])
            except CalledProcessError as err:  # pragma: no cover
                if err.returncode > 1:
                    # Exit codes >1 from gh-pr-upsert are not a problem for Commando.
                    pprint(err.stdout.rstrip())
                else:
                    raise
            else:
                pprint(result.stdout.rstrip())
        except CalledProcessError:  # pragma: no cover
            # Print the outputs of all the failed repo's commands.
            for result in results:
                print(f"$ {result.args} (returncode was: {result.returncode})")
                # Our run() helper pipes stderr to stdout so we only need to print stdout here.
                print(result.stdout)

            raise


def commando(
    repos, command, commit_message, branch, pr_title, pr_body
):  # pylint:disable=too-many-arguments,too-many-positional-arguments
    failed = False

    for repo in repos:
        try:
            _process_repo(repo, command, commit_message, branch, pr_title, pr_body)
        except CalledProcessError:  # pragma: no cover
            failed = True

    # Exit with 1 if any of the repos failed.
    return int(failed)
