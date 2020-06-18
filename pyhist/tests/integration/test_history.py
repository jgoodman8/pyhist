import os
import pickle
from typing import List

import pytest
from git import Repo

from pyhist.history.history import History
from pyhist.history.pyhist_item import PyHistItem
from pyhist.history.history_exception import HistoryException


class TestHistory:
    @pytest.fixture(scope="function")
    def git_repo(self) -> Repo:
        os.system("git init")
        repo = Repo(".git")

        os.system("touch testfile1")
        repo.git.add("testfile1")
        repo.git.commit("-m" "Add testfile1")

        os.system("touch testfile2")
        repo.git.add("testfile2")
        repo.git.commit("-m" "Add testfile2")

        yield repo

        os.system("rm testfile1")
        os.system("rm testfile2")
        os.system("rm -rf .git")

    @pytest.fixture(scope="function")
    def pyhist_items(self, git_repo: Repo) -> List[PyHistItem]:
        history = [
            PyHistItem(commit=commit, version=None, is_version=False)
            for commit in git_repo.iter_commits(git_repo.active_branch.name)
        ]

        with open(".pyhist", "wb") as f:
            pickle.dump(history, f)
            f.close()

        yield history

        os.system(f"rm .pyhist")

    def test_is_initialized_FileNotExists_ReturnsFalse(self):
        history = History()

        assert not history.is_initialized()

    def test_is_initialized_FileExists_ReturnsTrue(
        self, pyhist_items: List[PyHistItem]
    ):
        history = History()

        assert history.is_initialized()

    def test_load_history_FromInitializedFile_CommitsAreLoaded(
        self, pyhist_items: List[PyHistItem]
    ):
        history = History()

        history.load_history()

        assert history.pyhist_items == history.pyhist_items

    def test_load_history_FromInitializedFile_VersionsAreLoaded(
        self, pyhist_items: List[PyHistItem]
    ):
        history = History()

        history.load_history()

        assert history.pyhist_items == history.pyhist_items

    def test_load_history_NotInitialized_HistoryExceptionIsRaised(self):
        history = History()

        with pytest.raises(
            HistoryException,
            match='PyHist is not initialized. Please, type "pyhist --init"',
        ):
            history.load_history()

    def test_save_history_RemoveCommitAndSave_FileUpdatedWithoutCommit(
        self, pyhist_items: List[PyHistItem]
    ):
        # arrange
        history = History()
        history.load_history()

        # act
        history.remove_commit(history.pyhist_items[0].commit)
        history.save_history()

        # assert
        new_history = History()
        new_history.load_history()
        assert len(new_history.pyhist_items) == 1
        assert new_history.pyhist_items == history.pyhist_items
