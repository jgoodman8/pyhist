import os
import pickle
from typing import List, Optional

from git import Commit

from pyhist.history.pyhist_item import PyHistItem
from pyhist.history.history_exception import HistoryException
from pyhist.versioning.commit_type import CommitType
from pyhist.versioning.version import Version


class History:
    def __init__(self):
        self.__default_location = ".pyhist"
        self.pyhist_items: List[PyHistItem] = []

    def is_initialized(self) -> bool:
        return os.path.exists(self.__default_location)

    def load_history(self) -> None:
        if self.is_initialized():
            try:
                with open(self.__default_location, "rb") as file:
                    self.pyhist_items = pickle.load(file)
                    file.close()
            except IOError as e:
                raise HistoryException("Error loading pyhist history", e)
        else:
            raise HistoryException(
                'PyHist is not initialized. Please, type "pyhist --init"'
            )

    def save_history(self) -> None:
        try:
            with open(self.__default_location, "wb") as file:
                pickle.dump(self.pyhist_items, file)
                file.close()
        except IOError as e:
            raise HistoryException("Error updating pyhist history", e)

    def sync(self, added_commits: List[Commit], removed_commits: List[Commit]) -> None:
        for commit in removed_commits:
            if not self._is_versioning_commit(commit):
                self.remove_commit(commit)

        for commit in added_commits:
            if not self._is_versioning_commit(commit):
                self.add_commit(commit)

        self.save_history()

    def add_version(self, version: Version) -> None:
        item = PyHistItem(version=version, commit=None, is_version=True)
        self.pyhist_items.insert(0, item)

    def remove_version(self, version: Version) -> None:
        for item in self.pyhist_items:
            if item.version == version:
                self.pyhist_items.remove(item)

    def add_commit(self, commit: Commit) -> None:
        item = PyHistItem(version=None, commit=commit, is_version=False)
        self.pyhist_items.insert(0, item)

    def remove_commit(self, commit: Commit) -> None:
        for item in self.pyhist_items:
            if item.commit == commit:
                self.pyhist_items.remove(item)

    def has_any_version(self) -> bool:
        return any(item.is_version for item in self.pyhist_items)

    def get_version_items(self) -> List[PyHistItem]:
        return list(filter(lambda item: item.is_version, self.pyhist_items))

    def get_last_version(self) -> Optional[Version]:
        versions = self.get_version_items()
        return versions[0].version if len(versions) > 0 else None

    def is_initialized(self) -> bool:
        return os.path.exists(self.__default_location)

    @classmethod
    def _is_versioning_commit(cls, commit: Commit) -> bool:
        versioning_type = CommitType.Versioning.value
        return commit.message[: len(versioning_type)] == versioning_type
