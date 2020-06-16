import re
from typing import Tuple, Optional, Match, AnyStr

from pyhist.versioning.version_exception import VersionException


class SetupParser:
    def __init__(self, route: str = "setup.py"):
        self.file_route: str = route
        self.regex: str = "(version=['|\"])(.*)(['|\"])"

    def persist_version(self, version: str) -> None:
        file_content = self._read_setup_py()
        updated_content = re.sub(
            self.regex, repl=r"\g<1>{}\g<3>".format(version), string=file_content
        )
        self._rewrite_version(content=updated_content)

    def get_current_version_parts(self) -> Tuple[int, int, int]:
        version_str = self._get_version_str()
        return [int(version_part) for version_part in version_str.split(".")]

    def _read_setup_py(self) -> AnyStr:
        try:
            file = open(self.file_route, "r")
            file_content: AnyStr = file.read()
            file.close()

            return file_content
        except FileNotFoundError as e:
            raise VersionException("Cannot find setup.py", e)

    def _rewrite_version(self, content: str) -> None:
        try:
            file_writer = open(self.file_route, "w")
            file_writer.write(content)
            file_writer.close()
        except FileNotFoundError as e:
            raise VersionException("Cannot find setup.py", e)

    def _get_version_str(self) -> AnyStr:
        file_content: str = self._read_setup_py()

        version_match: Optional[Match[AnyStr]] = re.search(self.regex, file_content)
        if not version_match:
            raise Exception("")

        return version_match.group(2)
