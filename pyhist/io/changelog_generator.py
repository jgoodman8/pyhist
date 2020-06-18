from git import Commit

from pyhist.history.history import History
from pyhist.history.pyhist_item import PyHistItem


class ChangelogGenerator:
    def __init__(self, history: History):
        self.__history = history
        self.__changelog_route = "CHANGELOG.md"
        self.__repo_url = "https://github.com/jgoodman8/pyhist"
        self.__changelog_content = ""

    def generate_changelog(self) -> None:
        self._add_header()
        # self._add_new_version_title(version=new_version, is_breaking_change=is_breaking_change)
        for items in self.__history.pyhist_items:
            self._update_changelog_from_item(items)

        self._write()

    def _add_header(self):
        self.__changelog_content += "# Changelog\n\n"
        self.__changelog_content += (
            "All notable changes to this project will be documented in this file."
        )
        self.__changelog_content += (
            f"See [pyhist]({self.__repo_url}) for commit guidelines.\n"
        )

    def _update_changelog_from_item(self, item: PyHistItem) -> None:
        if item.is_version:
            self._add_version_entry(item, is_breaking_change=item.version.is_major)
        else:
            self._add_content_entry(item.commit)

    def _add_version_entry(self, item: PyHistItem, is_breaking_change: bool) -> None:
        version: str = item.version.get_version()
        date: str = item.version.date()

        breaking_change_text = " ⚠ BREAKING CHANGES " if is_breaking_change else " "
        self.__changelog_content += f"\n## {version}{breaking_change_text}({date})\n"

    def _add_content_entry(self, commit: Commit) -> None:
        date = self._get_commit_date(commit)
        message_parts = commit.message.split(":")

        if len(message_parts) >= 2:
            commit_type = message_parts[0]
            message = "".join(message_parts[1:])
            self.__changelog_content += f"- **{commit_type}**: {message} ({date})\n"
        else:
            self.__changelog_content += f"- {commit.message} ({date})\n"

    def _write(self) -> None:
        file = open(self.__changelog_route, "w")
        file.write(self.__changelog_content)
        file.close()

    @classmethod
    def _get_commit_date(cls, commit: Commit) -> str:
        return str(commit.committed_datetime.date())
