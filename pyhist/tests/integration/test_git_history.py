import os

import pytest

from pyhist.history.git_history import GitHistory


class TestGitHistory:
    @pytest.fixture(scope="function", autouse=True)
    def git(self):
        git_folder = ".git"
        os.system("git init")

        yield

        if os.path.exists(git_folder):
            os.system(f"rm -r {git_folder}")

        for file in os.listdir(os.curdir):
            if ".py" not in file:
                os.system(f"rm {file}")

    def test_load_history_NoCommitsAdded_LoadedCommitsAreEmpty(self, git):
        # arrange
        git_history = GitHistory()

        # act
        git_history.load_history()

        # assert
        assert len(git_history.git_commits) == 0

    def test_load_history_OneCommitAdded_LoadedCommitsHaveSizeOfOne(self, git):
        # arrange
        os.system("touch test.txt")
        os.system("git add test.txt")
        os.system('git commit -m "Initial commit"')

        git_history = GitHistory()

        # act
        git_history.load_history()

        # assert
        assert len(git_history.git_commits) == 1

    def test_load_history_TwoCommitsAdded_LoadedCommitsHaveSizeOfTwo(self, git):
        # arrange
        os.system("touch test.txt")
        os.system("git add test.txt")
        os.system('git commit -m "Initial commit"')
        os.system('echo "----" > test.txt')
        os.system("git add test.txt")
        os.system('git commit -m "Updated file"')

        git_history = GitHistory()

        # act
        git_history.load_history()

        # assert
        assert len(git_history.git_commits) == 2
