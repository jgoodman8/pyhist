import os

from click.testing import CliRunner, Result
from git import Repo

from pyhist.cli import main as cli
from pyhist.history import History
from pyhist.tests.validation.base_validation_test import BaseValidationTest


class TestCliInit(BaseValidationTest):
    def test_init_AddOneCommitBeforeInit_HistoryLoaded(self):
        # setup
        repo = Repo(self.git_folder)
        history = History()
        runner = CliRunner()

        # act
        # create and commit test file
        test_file = "test_file"
        os.system(f"touch {test_file}")
        repo.git.add(test_file)
        repo.git.commit("-m", "feat: Created test file")

        # init pyhist
        result: Result = runner.invoke(cli, ["--init"])

        # assert
        # assert cli result code
        assert result.exit_code == 0
        assert len(result.stdout) == 0

        # assert .pyhist is created
        current_dir_content = os.listdir(os.curdir)
        assert self.history_route in current_dir_content

        # assert git history is loaded by pyhist
        history.load_history()
        assert len(history.pyhist_items) == 2
        assert [item.version.get_version() for item in history.get_version_items()] == [
            "0.0.0"
        ]

    def test_init_AddTwoCommitsBeforeInit_HistoryLoaded(self):
        # setup
        repo = Repo(self.git_folder)
        history = History()
        runner = CliRunner()

        # act
        # create and commit test file
        test_file = "test_file"
        os.system(f"touch {test_file}")
        repo.git.add(test_file)
        repo.git.commit("-m", "feat: Created test file")
        os.system(f'echo "..." >> {test_file}')
        repo.git.add(test_file)
        repo.git.commit("-m", "fix: Updated file content")

        # init pyhist
        result: Result = runner.invoke(cli, ["--init"])

        # assert
        # assert cli result code
        assert result.exit_code == 0
        assert len(result.stdout) == 0

        # assert .pyhist is created
        current_dir_content = os.listdir(os.curdir)
        assert self.history_route in current_dir_content

        # assert git history is loaded by pyhist
        history.load_history()
        assert len(history.pyhist_items) == 3
        assert [item.version.get_version() for item in history.get_version_items()] == [
            "0.0.0"
        ]

    def test_init_AddVersioningCommitBeforeInit_VersionLoaded(self):
        # setup
        version = "0.0.1"
        repo = Repo(self.git_folder)
        history = History()
        runner = CliRunner()

        # act
        # create and commit test file
        changelog = "CHANGELOG.md"
        os.system(f"touch {changelog}")
        repo.git.add(changelog)
        repo.git.commit("-m", f"versioning: Set version {version}")

        # init pyhist
        result: Result = runner.invoke(cli, ["--init"])

        # assert
        # assert cli result code
        assert result.exit_code == 0
        assert len(result.stdout) == 0

        # assert .pyhist is created
        current_dir_content = os.listdir(os.curdir)
        assert self.history_route in current_dir_content

        # assert git history is loaded by pyhist
        history.load_history()
        assert len(history.pyhist_items) == 2

        assert len(history.get_version_items()) == 2
        assert [item.version.get_version() for item in history.get_version_items()] == [
            "0.0.0",
            version,
        ]

    def test_init_GitFileDoesNotExist_ErrorRaised(self):
        # setup
        os.system(f"rm -rf {self.git_folder}")
        runner = CliRunner()

        # act
        # init pyhist
        result: Result = runner.invoke(cli, ["--init"])

        # assert
        # assert cli result code and stderr
        assert result.exit_code == 0
        assert len(result.stdout) > 0
