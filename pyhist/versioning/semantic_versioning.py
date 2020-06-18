import re
from typing import List

from git import Commit

from pyhist.history.history import History
from pyhist.history.git_history import GitHistory
from pyhist.versioning.commit_type import CommitType
from pyhist.versioning.version import Version


class SemanticVersioning:
    def __init__(
        self, git_history: GitHistory, history: History,
    ):

        self.__git_history: GitHistory = git_history
        self.__history: History = history

        self.version: Version = None

    def update_version(
        self, added_commits: List[Commit], removed_commits: List[Commit]
    ) -> None:

        for commit in removed_commits:
            if self._is_release_commit(commit.message) or self.is_versioning_commit(
                commit.message
            ):
                self.version.create_from_version(
                    version=self.__history.get_last_version()
                )
            elif self._is_minor_change(commit.message):
                self.version.decrease_minor()
            elif self._is_patch_change(commit.message):
                self.version.decrease_patch()

        for commit in added_commits:
            if self.is_versioning_commit(commit.message):
                pass
            elif self._is_minor_change(commit.message):
                self.version.increase_minor()
            elif self._is_patch_change(commit.message):
                self.version.increase_patch()

        self.version.update()

    def generate_release(self) -> None:
        self.version.increase_major()

    @classmethod
    def _is_minor_change(cls, commit_message: str) -> bool:
        return cls._is_feature(commit_message)

    @classmethod
    def _is_patch_change(cls, commit_message: str) -> bool:
        return (
            cls._is_fix(commit_message)
            or cls._is_refactor(commit_message)
            or cls._is_docs(commit_message)
            or cls._is_test(commit_message)
            or cls._is_style(commit_message)
            or cls._is_chore(commit_message)
            or cls._is_performance(commit_message)
        )

    @classmethod
    def _is_release_commit(cls, commit_message: str) -> bool:
        return cls._check_semantic_commit(
            commit_message, commit_type=CommitType.Release.value
        )

    @classmethod
    def is_versioning_commit(cls, commit_message: str) -> bool:
        return cls._check_semantic_commit(
            commit_message, commit_type=CommitType.Versioning.value
        )

    @classmethod
    def _is_feature(cls, commit_message: str) -> bool:
        return cls._check_semantic_commit(
            commit_message, commit_type=CommitType.Feature.value
        )

    @classmethod
    def _is_fix(cls, commit_message: str) -> bool:
        return cls._check_semantic_commit(
            commit_message, commit_type=CommitType.Fix.value
        )

    @classmethod
    def _is_refactor(cls, commit_message: str) -> bool:
        return cls._check_semantic_commit(
            commit_message, commit_type=CommitType.Refactor.value
        )

    @classmethod
    def _is_performance(cls, commit_message: str) -> bool:
        return cls._check_semantic_commit(
            commit_message, commit_type=CommitType.Performance.value
        )

    @classmethod
    def _is_docs(cls, commit_message: str) -> bool:
        return cls._check_semantic_commit(
            commit_message, commit_type=CommitType.Docs.value
        )

    @classmethod
    def _is_test(cls, commit_message: str) -> bool:
        return cls._check_semantic_commit(
            commit_message, commit_type=CommitType.Test.value
        )

    @classmethod
    def _is_chore(cls, commit_message: str) -> bool:
        return cls._check_semantic_commit(
            commit_message, commit_type=CommitType.Chore.value
        )

    @classmethod
    def _is_style(cls, commit_message: str) -> bool:
        return cls._check_semantic_commit(
            commit_message, commit_type=CommitType.Style.value
        )

    @classmethod
    def _check_semantic_commit(cls, commit_message: str, commit_type: str) -> bool:
        return commit_message[: len(commit_type)] == commit_type

    @classmethod
    def parse_version_from_commit(cls, commit: Commit) -> Version:
        version_match = re.search(r"(.*)([0-9]\.[0-9]\.[0-9])(.*)", commit.message)

        if version_match is not None and version_match.lastindex == 3:
            return Version().create_from_str_version(version_match[2])
