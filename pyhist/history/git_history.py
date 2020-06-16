import os
from typing import List

from git import Commit, Repo, GitCommandError, Diff
from gitdb.exc import BadName


class GitHistory:
    def __init__(self):
        self.__root = ".git"
        self.__setup_file = "setup.py"
        self.__changelog_file = "CHANGELOG.md"
        self.__pyhist_file = ".pyhist"
        self.__repo: Repo = None
        self.git_commits: List[Commit] = []

    def has_git_support(self) -> bool:
        return os.path.exists(self.__root)

    def load_history(self) -> None:
        try:
            self.__repo = Repo(self.__root)
            self.git_commits = self._get_commits()
        except Exception as e:
            print(e)  # TODO: use logger

    def get_commit_ids(self) -> List[str]:
        return [commit.hexsha for commit in self.git_commits]

    def add_versioning_commit(self, version: str) -> None:
        untracked_files = self._get_untracked_files()

        if (
            self.__changelog_file in untracked_files
            or self.__setup_file in untracked_files
            or self.__pyhist_file in untracked_files
        ):

            if self.__setup_file in untracked_files:
                self.__repo.index.add(self.__setup_file)
            if self.__changelog_file in untracked_files:
                self.__repo.index.add(self.__changelog_file)
            if self.__pyhist_file in untracked_files:
                self.__repo.index.add(self.__pyhist_file)

            self.__repo.git.commit("-m", f"versioning: Set version to {version}")

    def add_initial_commit(self, version: str) -> None:
        untracked_files = self._get_untracked_files()

        if self.__pyhist_file in untracked_files:
            self.__repo.index.add(self.__pyhist_file)
            self.__repo.git.commit(
                "-m", f"versioning: Init pyhist with version {version}"
            )

    def _get_commits(self) -> List[Commit]:
        try:
            return [
                commit
                for commit in self.__repo.iter_commits(self.__repo.active_branch.name)
            ]
        except GitCommandError:
            return []

    @classmethod
    def _process_commit_message(cls, commit_message: str) -> str:
        if "\n" not in commit_message:
            return commit_message

        return commit_message.split("\n")[0]

    def _get_untracked_files(self) -> List[str]:
        try:
            diff: List[Diff] = self.__repo.index.diff("HEAD") + self.__repo.index.diff(
                None
            )
            return [
                file.a_path or file.b_path for file in diff
            ] + self.__repo.untracked_files
        except BadName:
            return self.__repo.untracked_files
