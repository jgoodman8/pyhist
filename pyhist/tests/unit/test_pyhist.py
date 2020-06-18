from typing import List
from unittest.mock import patch, MagicMock, Mock

from git import Commit

from pyhist.history.git_history import GitHistory
from pyhist.history.history import History
from pyhist.history.pyhist_item import PyHistItem
from pyhist.io.changelog_generator import ChangelogGenerator
from pyhist.io.setup_parser import SetupParser
from pyhist.pyhist import PyHist
from pyhist.versioning.semantic_versioning import SemanticVersioning
from pyhist.versioning.version import Version


class TestPyHist:
    def test_setup_NoPreviousCommits_NoCommitsAdded(self):
        # arrange
        git_history = MagicMock()
        history = MagicMock()
        semantic_versioning = MagicMock()
        changelog_generator = MagicMock()
        setup_parser = MagicMock()

        pyhist = PyHist(
            git_history=git_history,
            history=history,
            semantic_versioning=semantic_versioning,
            changelog_generator=changelog_generator,
            setup_parser=setup_parser,
        )

        # act
        with patch.object(
            history, "is_initialized", return_value=False
        ) as patch_is_initialized, patch.object(
            setup_parser, "get_current_version_parts", return_value=(0, 0, 1)
        ) as patch_get_current_version_parts:
            pyhist.setup()

            # assert
            assert not history.add_commit.called
            assert history.save_history.called
            assert history.add_version.called
            assert patch_is_initialized.called
            assert patch_get_current_version_parts.called
            assert git_history.add_initial_commit.called_once_with(version="0.0.1")

    def test_setup_WithPreviousCommits_PreviousCommitsAdded(self):
        # arrange
        git_history = MagicMock()
        history = MagicMock()
        semantic_versioning = MagicMock()
        changelog_generator = MagicMock()
        setup_parser = MagicMock()
        git_commits = [MagicMock(), MagicMock()]

        pyhist = PyHist(
            git_history=git_history,
            history=history,
            semantic_versioning=semantic_versioning,
            changelog_generator=changelog_generator,
            setup_parser=setup_parser,
        )

        # act
        with patch.object(
            history, "is_initialized", return_value=False
        ) as patch_is_initialized, patch.object(
            setup_parser, "get_current_version_parts", return_value=(0, 0, 1)
        ) as patch_get_current_version_parts:
            pyhist.setup()

            # assert
            for commit_id in git_commits:
                assert history.add_commit.called_once_with(commit_id)
            assert history.save_history.called
            assert history.save_history.called
            assert history.add_version.called
            assert patch_is_initialized.called
            assert patch_get_current_version_parts.called
            assert git_history.add_initial_commit.called_once_with(version="0.0.1")

    def test_update_FeatureAdded_MinorIncreased(self):
        self.assert_version_update(
            current_version=None,
            git_commits=[b"11111111111111111111", b"22222222222222222222"],
            git_commits_messages=["Initial commit", "feat: commit message"],
            pyhist_commits=[],
            pyhist_commits_messages=[],
            expected_version="0.1.0",
        )

    def test_update_FeatureRemoved_MinorDecreased(self):
        self.assert_version_update(
            current_version="0.1.0",
            git_commits=[b"11111111111111111111"],
            git_commits_messages=["Initial commit"],
            pyhist_commits=[b"11111111111111111111", b"22222222222222222222"],
            pyhist_commits_messages=["Initial commit", "feat: commit message"],
            expected_version="0.0.0",
        )

    def test_update_ChangesInHistory_VersionUpdated(self):
        self.assert_version_update(
            current_version="0.1.0",
            git_commits=[b"11111111111111111111", b"22222222222222222222"],
            git_commits_messages=["Initial commit", "fix: Temporal fix"],
            pyhist_commits=[b"11111111111111111111", b"33333333333333333333"],
            pyhist_commits_messages=["Initial commit", "feat: commit message"],
            expected_version="0.0.1",
        )

    def test_update_FixAndRefactorAdded_PatchIncreasedByTwo(self):
        self.assert_version_update(
            current_version="0.1.0",
            git_commits=[
                b"11111111111111111111",
                b"22222222222222222222",
                b"33333333333333333333",
                b"44444444444444444444",
            ],
            git_commits_messages=[
                "Initial commit",
                "feat: commit message",
                "fix: Temporal fix",
                "refactor: Code Refactor",
            ],
            pyhist_commits=[b"11111111111111111111", b"22222222222222222222"],
            pyhist_commits_messages=["Initial commit", "feat: commit message"],
            expected_version="0.1.2",
        )

    def test_update_AmendWithSameMessage_NoChangesInVersion(self):
        self.assert_version_update(
            current_version="0.1.0",
            git_commits=[b"11111111111111111111", b"33333333333333333333"],
            git_commits_messages=["Initial commit", "feat: commit message"],
            pyhist_commits=[b"11111111111111111111", b"22222222222222222222"],
            pyhist_commits_messages=["Initial commit", "feat: commit message"],
            expected_version="0.1.0",
        )

    @classmethod
    def assert_version_update(
        cls,
        current_version: str,
        git_commits: List[str],
        git_commits_messages: List[str],
        pyhist_commits: List[str],
        pyhist_commits_messages: List[str],
        expected_version: str,
    ):

        git_history = GitHistory()
        git_history.git_commits = cls.build_commits(
            commits=git_commits, messages=git_commits_messages
        )

        history = History()
        history.pyhist_items = [
            PyHistItem(commit=commit, version=None, is_version=False)
            for commit in cls.build_commits(
                commits=pyhist_commits, messages=pyhist_commits_messages
            )
        ]
        if current_version is not None:
            history.pyhist_items.insert(
                0,
                PyHistItem(
                    commit=None,
                    version=Version().create_from_str_version(current_version),
                    is_version=False,
                ),
            )

        setup_parser = SetupParser()
        current_version_parts = (
            [0, 0, 0]
            if current_version is None
            else [int(part) for part in current_version.split(".")]
        )
        changelog_generator = ChangelogGenerator(history=history)
        semantic_versioning = SemanticVersioning(
            git_history=git_history, history=history
        )

        pyhist = PyHist(
            git_history=git_history,
            history=history,
            semantic_versioning=semantic_versioning,
            changelog_generator=changelog_generator,
            setup_parser=setup_parser,
        )

        # act
        with patch.object(
            setup_parser, "persist_version"
        ) as patch_persist_version, patch.object(
            setup_parser,
            "get_current_version_parts",
            return_value=current_version_parts,
        ) as patch_get_current_version_parts, patch.object(
            git_history, "add_versioning_commit"
        ) as patch_add_versioning_commit, patch.object(
            history, "load_history", side_effect=lambda: None
        ) as patch_load_history, patch.object(
            history, "save_history", side_effect=lambda: None
        ) as patch_save_history, patch.object(
            changelog_generator, "generate_changelog", side_effect=lambda: None
        ) as patch_generate_changelog:
            pyhist.update()

        # assert
        assert patch_add_versioning_commit.called_once_with(
            version=expected_version, is_release=False
        )
        assert patch_save_history.called
        assert patch_load_history.called
        assert patch_generate_changelog.called
        assert patch_get_current_version_parts.called
        assert patch_persist_version.called_once_with(version=expected_version)

    @classmethod
    def build_commits(cls, commits: List[str], messages: List[str]) -> List[Commit]:
        return [
            Commit(repo=Mock(), binsha=commit, message=message)
            for commit, message in zip(commits, messages)
        ]
