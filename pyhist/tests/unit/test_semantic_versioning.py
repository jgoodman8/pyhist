from typing import List
from unittest.mock import MagicMock, Mock

from git import Commit

from pyhist.history.history import History
from pyhist.history.git_history import GitHistory
from pyhist.versioning.semantic_versioning import SemanticVersioning
from pyhist.versioning.version import Version


class TestSemanticVersioning:
    def test_update_FixAdded_PatchIncreased(self):
        added_commits = self.create_commits(
            ids=[b"11111111111111111111", b"22222222222222222222"],
            messages=["Initial commit", "fix: commit message"],
        )

        self.assert_version_update(
            current_version=Version().create_from_str_version("0.0.1"),
            added_commits=added_commits,
            removed_commits=[],
            expected_version=Version().create_from_str_version("0.0.2"),
        )

    def test_update_FeatureAdded_MinorIncreased(self):
        added_commits = self.create_commits(
            ids=[b"11111111111111111111", b"22222222222222222222"],
            messages=["Initial commit", "feat: commit message"],
        )

        self.assert_version_update(
            current_version=Version().create_from_str_version("0.0.0"),
            added_commits=added_commits,
            removed_commits=[],
            expected_version=Version().create_from_str_version("0.1.0"),
        )

    def test_update_FeatureRemoved_MinorDecreased(self):
        removed_commits = self.create_commits(
            ids=[b"22222222222222222222"], messages=["feat: commit message"]
        )

        self.assert_version_update(
            current_version=Version().create_from_str_version("0.1.0"),
            added_commits=[],
            removed_commits=removed_commits,
            expected_version=Version().create_from_str_version("0.0.0"),
        )

    def test_update_ChangesInHistory_VersionUpdated(self):
        added_commits = self.create_commits(
            ids=[b"33333333333333333333"], messages=["fix: Temporal fix"]
        )
        removed_commits = self.create_commits(
            ids=[b"22222222222222222222"], messages=["feat: commit message"]
        )

        self.assert_version_update(
            current_version=Version().create_from_str_version("0.1.0"),
            added_commits=added_commits,
            removed_commits=removed_commits,
            expected_version=Version().create_from_str_version("0.0.1"),
        )

    def test_update_FixAndRefactorAdded_PatchIncreasedByTwo(self):
        added_commits = self.create_commits(
            ids=[b"33333333333333333333", b"44444444444444444444"],
            messages=["fix: Temporal fix", "refactor: Code Refactor"],
        )

        self.assert_version_update(
            current_version=Version().create_from_str_version("0.1.0"),
            added_commits=added_commits,
            removed_commits=[],
            expected_version=Version().create_from_str_version("0.1.2"),
        )

    def test_update_AmendWithSameMessage_NoChangesInVersion(self):
        added_commits = self.create_commits(
            ids=[b"33333333333333333333"], messages=["feat: commit message updated"]
        )
        removed_commits = self.create_commits(
            ids=[b"22222222222222222222"], messages=["feat: commit message"]
        )

        self.assert_version_update(
            current_version=Version().create_from_str_version("0.1.0"),
            added_commits=added_commits,
            removed_commits=removed_commits,
            expected_version=Version().create_from_str_version("0.1.0"),
        )

    @staticmethod
    def assert_version_update(
        current_version: Version,
        added_commits: List[Commit],
        removed_commits: List[Commit],
        expected_version: Version,
    ):
        git_history = GitHistory()
        history = History()
        version_parser = MagicMock()

        semantic_versioning = SemanticVersioning(
            git_history=git_history, history=history
        )
        semantic_versioning.version = current_version

        # act
        semantic_versioning.update_version(
            added_commits=added_commits, removed_commits=removed_commits
        )

        # assert
        assert version_parser.persist_current_version.called_once_with(
            version=expected_version.get_version()
        )

    @classmethod
    def create_commits(cls, ids: List[str], messages: List[str]) -> List[Commit]:
        return [
            Commit(repo=Mock(), binsha=commit, message=message)
            for commit, message in zip(ids, messages)
        ]
