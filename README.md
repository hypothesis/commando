<a href="https://github.com/hypothesis/commando/actions/workflows/ci.yml?query=branch%3Amain"><img src="https://img.shields.io/github/actions/workflow/status/hypothesis/commando/ci.yml?branch=main"></a>
<a><img src="https://img.shields.io/badge/python-3.12 | 3.11 | 3.10 | 3.9-success"></a>
<a href="https://github.com/hypothesis/commando/blob/main/LICENSE"><img src="https://img.shields.io/badge/license-BSD--2--Clause-success"></a>
<a href="https://github.com/hypothesis/cookiecutters/tree/main/pypackage"><img src="https://img.shields.io/badge/cookiecutter-pypackage-success"></a>
<a href="https://black.readthedocs.io/en/stable/"><img src="https://img.shields.io/badge/code%20style-black-000000"></a>

# Commando

Run commands in repos and send any resulting changes as PRs.

Commando clones a given list of GitHub repos, runs a given command in each
repo, and sends any resulting changes as pull requests (PRs) to each repo.

### Usage

For example lets send PRs to repo-1, repo-2 and repo-3 to add a copyright notice to the bottom
of each repo's `README.md` file:

```console
$ commando --repos hypothesis/repo-1 hypothesis/repo-2 hypothesis/repo-3 \
           --command 'echo "Copyright (c) 2022 Me" >> README.md' \
           --branch add-copyright-notice \
           --commit-message 'Add a copyright notice to the README' \
           --pr-title 'Add a copyright notice to the README'
```

See `commando --help` for the full list of command line options.

You can give a hard-coded list of repos like in the command above or you can
use a command to generate the `--repos` argument. For example we can use
[GitHub CLI](https://cli.github.com/)'s
[`gh api`](https://cli.github.com/manual/gh_api) command to call the GitHub
REST API's [search repositories](https://docs.github.com/en/rest/search?apiVersion=2022-11-28#search-repositories)
API and get a list of all repos in the hypothesis organization that have the
text `cookiecutter.json` in their README file. We can then run `make template`
to update each repo with any changes from [our cookiecutter templates](https://github.com/hypothesis/cookiecutters):

```console
$ commando --repos $(gh api -X GET search/repositories --paginate -f 'q=cookiecutter.json in:readme org:hypothesis archived:false' -q '.items | .[] | .full_name' | xargs) \
           --command 'make template'
           --branch cookiecutter
           --commit-message 'Apply updates from cookiecutter'
           --pr-title 'Apply updates from cookiecutter'
```

## Installing

We recommend using [pipx](https://pypa.github.io/pipx/) to install
Commando.
First [install pipx](https://pypa.github.io/pipx/#install-pipx) then run:

```terminal
pipx install git+https://github.com/hypothesis/commando.git
```

You now have Commando installed! For some help run:

```
commando --help
```

## Upgrading

To upgrade to the latest version run:

```terminal
pipx upgrade commando
```

To see what version you have run:

```terminal
commando --version
```

## Uninstalling

To uninstall run:

```
pipx uninstall commando
```

## Setting up Your Commando Development Environment

First you'll need to install:

* [Git](https://git-scm.com/).
  On Ubuntu: `sudo apt install git`, on macOS: `brew install git`.
* [GNU Make](https://www.gnu.org/software/make/).
  This is probably already installed, run `make --version` to check.
* [pyenv](https://github.com/pyenv/pyenv).
  Follow the instructions in pyenv's README to install it.
  The **Homebrew** method works best on macOS.
  The **Basic GitHub Checkout** method works best on Ubuntu.
  You _don't_ need to set up pyenv's shell integration ("shims"), you can
  [use pyenv without shims](https://github.com/pyenv/pyenv#using-pyenv-without-shims).

Then to set up your development environment:

```terminal
git clone https://github.com/hypothesis/commando.git
cd commando
make help
```

## Changing the Project's Python Versions

To change what versions of Python the project uses:

1. Change the Python versions in the
   [cookiecutter.json](.cookiecutter/cookiecutter.json) file. For example:

   ```json
   "python_versions": "3.10.4, 3.9.12",
   ```

2. Re-run the cookiecutter template:

   ```terminal
   make template
   ```

3. Commit everything to git and send a pull request

## Changing the Project's Python Dependencies

To change the production dependencies in the `setup.cfg` file:

1. Change the dependencies in the [`.cookiecutter/includes/setuptools/install_requires`](.cookiecutter/includes/setuptools/install_requires) file.
   If this file doesn't exist yet create it and add some dependencies to it.
   For example:

   ```
   pyramid
   sqlalchemy
   celery
   ```

2. Re-run the cookiecutter template:

   ```terminal
   make template
   ```

3. Commit everything to git and send a pull request

To change the project's formatting, linting and test dependencies:

1. Change the dependencies in the [`.cookiecutter/includes/tox/deps`](.cookiecutter/includes/tox/deps) file.
   If this file doesn't exist yet create it and add some dependencies to it.
   Use tox's [factor-conditional settings](https://tox.wiki/en/latest/config.html#factors-and-factor-conditional-settings)
   to limit which environment(s) each dependency is used in.
   For example:

   ```
   lint: flake8,
   format: autopep8,
   lint,tests: pytest-faker,
   ```

2. Re-run the cookiecutter template:

   ```terminal
   make template
   ```

3. Commit everything to git and send a pull request
