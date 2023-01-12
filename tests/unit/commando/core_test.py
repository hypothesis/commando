from unittest.mock import sentinel

import pytest

from commando.core import commando


class TestCommando:
    def test_it(self):
        exit_status = commando(
            [sentinel.repo_1, sentinel.repo_2],
            ["test", "command"],
            sentinel.commit_message,
            sentinel.branch,
            sentinel.pr_title,
            sentinel.pr_body,
        )

        assert not exit_status

    @pytest.fixture(autouse=True)
    def subprocess(self, mocker):
        return mocker.patch("commando.core.subprocess", autospec=True)
