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
