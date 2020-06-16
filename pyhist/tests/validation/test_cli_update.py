import os
from typing import List

from click.testing import CliRunner, Result
from git import Repo

from pyhist.cli import main as cli
from pyhist.history import History
from pyhist.io.setup_parser import SetupParser
from pyhist.tests.validation.base_validation_test import BaseValidationTest


class TestCliUpdate(BaseValidationTest):
    def test_update_AddFeature_Version010IsSet(self):
        # setup
        repo = Repo(self.git_folder)

        # act
        # init pyhist
        init_result: Result = CliRunner().invoke(cli, ["--init"])

        self.assert_init(["0.0.0"], init_result)

        # create and commit test file
        test_file = "test_file"
        os.system(f"touch {test_file}")
        repo.git.add(test_file)
        repo.git.commit("-m", "feat: Created test file")

        # execute update
        update_result: Result = CliRunner().invoke(cli, ["--update"])

        self.asserts(["0.1.0", "0.0.0"], update_result, repo)

    def test_update_AddFix_Version001IsSet(self):
        # setup
        repo = Repo(self.git_folder)

        # act
        # init pyhist
        init_result: Result = CliRunner().invoke(cli, ["--init"])

        self.assert_init(["0.0.0"], init_result)

        # create and commit test file
        test_file = "test_file"
        os.system(f"touch {test_file}")
        repo.git.add(test_file)
        repo.git.commit("-m", "fix: Created test file")

        # execute update
        update_result: Result = CliRunner().invoke(cli, ["--update"])

        self.asserts(["0.0.1", "0.0.0"], update_result, repo)

    def test_update_AddTwoFixes_Version002IsSet(self):
        # setup
        repo = Repo(self.git_folder)

        # act
        # init pyhist
        init_result: Result = CliRunner().invoke(cli, ["--init"])

        self.assert_init(["0.0.0"], init_result)

        # create and commit test file
        test_file = "test_file"
        os.system(f"touch {test_file}")
        repo.git.add(test_file)
        repo.git.commit("-m", "fix: Created test file")

        # execute update
        update_result: Result = CliRunner().invoke(cli, ["--update"])

        self.asserts(["0.0.1", "0.0.0"], update_result, repo)

        # create and commit test file
        os.system(f'echo "text" >> {test_file}')
        repo.git.add(test_file)
        repo.git.commit("-m", "fix: Updated test file")

        # execute update
        update_result: Result = CliRunner().invoke(cli, ["--update"])

        self.asserts(["0.0.2", "0.0.1", "0.0.0"], update_result, repo)

    def test_update_InitCheckoutNewBranchAddFeatureAndCheckoutToMaster_Version010IsSetInBranchAndMasterIsEmpty(
        self,
    ):
        # setup
        test_file = "test_file"
        repo = Repo(self.git_folder)
        history = History()

        # act
        # create initial commit
        os.system(f"touch {test_file}")
        repo.git.add(test_file)
        repo.git.commit("-m", "Initial commit")

        # init pyhist
        init_result: Result = CliRunner().invoke(cli, ["--init"])

        self.assert_init(["0.0.0"], init_result)

        # assert pyhist commits and versions
        history.load_history()
        assert len(history.pyhist_items) == 2

        # checkout to new branch
        repo.git.checkout("HEAD", b="new_branch")

        # create and commit test file
        os.system(f'echo "..." >> {test_file}')
        repo.git.add(test_file)
        repo.git.commit("-m", "fix: Create test file")

        # execute update
        update_result: Result = CliRunner().invoke(cli, ["--update"])

        # assert
        self.asserts(["0.0.1", "0.0.0"], update_result, repo)

        history.load_history()
        assert len(history.pyhist_items) == 4

        # checkout to  master
        repo.heads.master.checkout()

        # assert pyhist commits and versions
        history.load_history()
        assert len(history.pyhist_items) == 2

        assert "setup.py" not in repo.untracked_files
        assert ".pyhist" not in repo.untracked_files
        assert "CHANGELOG.md" not in repo.untracked_files

    @staticmethod
    def asserts(
        expected_versions: List[str], result: Result, repo: Repo,
    ):
        # assert
        # assert cli result codes
        assert result.exit_code == 0
        assert len(result.stdout) == 0

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

    @staticmethod
    def assert_init(
        expected_versions: List[str], result: Result,
    ):
        # assert
        # assert cli result codes
        assert result.exit_code == 0
        assert len(result.stdout) == 0

        # assert expected version set
        parser = SetupParser()
        assert parser._get_version_str() == expected_versions[0]

        # assert version is add to pyhist
        history = History()
        history.load_history()
        assert [
            item.version.get_version() for item in history.get_version_items()
        ] == expected_versions
