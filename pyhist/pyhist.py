import copy
from typing import List

from git import Commit

from pyhist.history.history import History
from pyhist.history.git_history import GitHistory
from pyhist.io.changelog_generator import ChangelogGenerator
from pyhist.io.setup_parser import SetupParser
from pyhist.versioning.semantic_versioning import SemanticVersioning
from pyhist.versioning.version import Version


class PyHist:
    def __init__(
        self,
        history: History,
        git_history: GitHistory,
        semantic_versioning: SemanticVersioning,
        changelog_generator: ChangelogGenerator,
        setup_parser: SetupParser,
    ):

        self.history: History = history
        self.git_history: GitHistory = git_history
        self.changelog_generator: ChangelogGenerator = changelog_generator

        self.__semantic_versioning: SemanticVersioning = semantic_versioning
        self.__setup_parser: SetupParser = setup_parser

        self.__added_commits = None
        self.__removed_commits = None
        self.__versioning_commit = None

    def setup(self):
        if not self.git_history.has_git_support():
            print("This repository has not git support")
            return
        if self.history.is_initialized():
            print("Pyhist is already initialized")
            return

        self.git_history.load_history()
        self._init_pyhist()
        self._generate_initial_version()

    def update(self) -> None:
        self.git_history.load_history()
        self.history.load_history()

        self._get_version_updates()

        if self._any_updates():
            self._perform_version_changes()

    def major(self) -> None:
        # Load history
        self.git_history.load_history()
        self.history.load_history()

        # Set previous version
        self.__semantic_versioning.version = self._get_previous_version()

        # Update to release version
        self.__semantic_versioning.generate_release()

        self._perform_version_changes()

    def _get_version_updates(self) -> None:
        # Set previous version
        self.__semantic_versioning.version = self._get_previous_version()

        # Get changes with respect to current .pyhist
        self.__added_commits = self._get_added_commits()
        self.__removed_commits = self._get_removed_commits()

        # Sync pyhist history
        self.history.sync(
            added_commits=self.__added_commits, removed_commits=self.__removed_commits
        )

        # Get current version and calculate new version
        self.__semantic_versioning.update_version(
            added_commits=self.__added_commits, removed_commits=self.__removed_commits
        )

    def _perform_version_changes(self) -> None:
        # Update version
        self.__semantic_versioning.version.update()

        # Version to be set
        updated_version = self.__semantic_versioning.version

        # Update version in setup.py
        self.__setup_parser.persist_version(version=updated_version.get_version())

        # Add version to pyhist history and save
        self.history.add_version(version=updated_version)
        self.history.save_history()

        # Generate changelog
        self.changelog_generator.generate_changelog()

        # Create versioning commit with changelog.md, setup.py and .pyhist changes
        self.git_history.add_versioning_commit(version=updated_version.get_version())

    def _get_added_commits(self) -> List[Commit]:
        current_pyhist_commit_ids = [
            item.commit.hexsha
            for item in self.history.pyhist_items
            if item.commit is not None
        ]

        filtered_commits = filter(
            lambda commit: commit.hexsha not in current_pyhist_commit_ids,
            self.git_history.git_commits,
        )

        return list(filtered_commits)

    def _get_removed_commits(self) -> List[Commit]:
        git_commit_ids = [commit.hexsha for commit in self.git_history.git_commits]
        filtered_items = filter(
            lambda item: item.commit is not None
            and item.commit.hexsha not in git_commit_ids,
            self.history.pyhist_items,
        )

        return [item.commit for item in filtered_items]

    def _any_updates(self) -> bool:
        return len(self.__added_commits) or len(self.__removed_commits)

    def _get_previous_version(self) -> None:
        previous_version = self.history.get_last_version()
        if previous_version is not None:
            return copy.deepcopy(previous_version)

        return Version().create_from_version_parts(
            *self.__setup_parser.get_current_version_parts()
        )

    def _init_pyhist(self) -> None:
        for commit in self.git_history.git_commits:
            if not self.__semantic_versioning.is_versioning_commit(commit.message):
                self.history.add_commit(commit)
            else:
                # TODO: Move parse method
                version = self.__semantic_versioning.parse_version_from_commit(commit)
                self.history.add_version(version=version)

    def _generate_initial_version(self) -> None:
        initial_version = Version().create_from_version_parts(
            *self.__setup_parser.get_current_version_parts()
        )
        self.history.add_version(version=initial_version)
        self.history.save_history()
        self.git_history.add_initial_commit(version=initial_version.get_version())
