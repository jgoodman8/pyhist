import os
from typing import List

from click.testing import CliRunner, Result
from git import Repo

from pyhist.cli import main as cli
from pyhist.history import History
from pyhist.io.setup_parser import SetupParser
from pyhist.tests.validation.base_validation_test import BaseValidationTest


class TestCliMajor(BaseValidationTest):
    def test_release_CreateRelease_Version100IsSet(self):
        # setup
        repo = Repo(self.git_folder)

        # act
        # init pyhist
        init_result: Result = CliRunner().invoke(cli, ["--init"])

        # create and commit test file
        test_file = "test_file"
        os.system(f"touch {test_file}")
        repo.git.add(test_file)
        repo.git.commit("-m", "feat: Created test file")

        # execute release
        release_result: Result = CliRunner().invoke(cli, ["--major"])

        self.asserts(["1.0.0", "0.0.0"], init_result, release_result, repo)

    def test_release_CreateUpdateFixAndRelease_Version010And011And100AreSet(self):
        # setup
        repo = Repo(self.git_folder)

        # act
        # init pyhist
        init_result: Result = CliRunner().invoke(cli, ["--init"])

        # create and commit test file
        test_file = "test_file"
        os.system(f"touch {test_file}")
        repo.git.add(test_file)
        repo.git.commit("-m", "feat: Created test file")

        # execute update
        update_result: Result = CliRunner().invoke(cli, ["--update"])
        self.asserts(["0.1.0", "0.0.0"], init_result, update_result, repo)

        # create and commit test file
        test_file = "test_file"
        os.system(f'echo "text" >> {test_file}')
        repo.git.add(test_file)
        repo.git.commit("-m", "fix: Created test file")

        # execute update
        update_result: Result = CliRunner().invoke(cli, ["--update"])
        self.asserts(["0.1.1", "0.1.0", "0.0.0"], init_result, update_result, repo)

        # execute release
        release_result: Result = CliRunner().invoke(cli, ["--major"])

        self.asserts(
            ["1.0.0", "0.1.1", "0.1.0", "0.0.0"], init_result, release_result, repo
        )

    @staticmethod
    def asserts(
        expected_versions: List[str],
        init_result: Result,
        update_result: Result,
        repo: Repo,
    ):
        # assert
        # assert cli result codes
        assert init_result.exit_code == 0
        assert len(init_result.stdout) == 0
        assert update_result.exit_code == 0
        assert len(update_result.stdout) == 0

        # assert changelog is created
        assert "CHANGELOG.md" in os.listdir(os.curdir)

        # assert expected version set
        parser = SetupParser()
        assert parser._get_version_str() == expected_versions[0]

        # assert version is add to pyhist
        history = History()
        history.load_history()
        assert [
            item.version.get_version() for item in history.get_version_items()
        ] == expected_versions

        assert "setup.py" not in repo.untracked_files
        assert ".pyhist" not in repo.untracked_files
        assert "CHANGELOG.md" not in repo.untracked_files
