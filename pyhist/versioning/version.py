from datetime import datetime
from typing import Optional


class Version:
    def __init__(self):
        self.major = None
        self.minor = None
        self.patch = None

        self.__updated_major = None
        self.__updated_minor = None
        self.__updated_patch = None

        self.is_major = False
        self.__version_timestamp: float = None

    # Constructor
    def create_from_str_version(self, version: str) -> "Version":
        self.set_version(*[int(part) for part in version.split(".")])
        return self

    # Constructor
    def create_from_version(self, version: "Version") -> "Version":
        self.set_version(major=version.major, minor=version.minor, patch=version)
        return self

    # Constructor
    def create_from_version_parts(
        self, major: int, minor: int, patch: int
    ) -> "Version":
        self.set_version(major=major, minor=minor, patch=patch)
        return self

    # Constructor
    def set_version(self, major: int, minor: int, patch: int) -> None:
        self.major = major
        self.minor = minor
        self.patch = patch

        self.__updated_major = major
        self.__updated_minor = minor
        self.__updated_patch = patch

    def get_version(self) -> str:
        return f"{self.major}.{self.minor}.{self.patch}"

    def increase_minor(self) -> None:
        self.__updated_minor += 1
        self.__updated_patch = 0

    def increase_major(self) -> None:
        self.__updated_major += 1
        self.__updated_minor = 0
        self.__updated_patch = 0

    def increase_patch(self) -> None:
        self.__updated_patch += 1

    def decrease_minor(self) -> None:
        self.__updated_minor -= 1

    def decrease_patch(self) -> None:
        self.__updated_patch -= 1

    def has_changed(self) -> bool:
        return (
            self.__updated_major != self.major
            or self.__updated_minor != self.minor
            or self.__updated_patch != self.patch
        )

    def update(self):
        if self.has_changed():
            if self.major < self.__updated_major:
                self.is_major = True

            self.major = self.__updated_major
            self.minor = self.__updated_minor
            self.patch = self.__updated_patch

            self.__version_timestamp = datetime.utcnow().timestamp()

    def date(self) -> Optional[str]:
        if self.__version_timestamp:
            return datetime.fromtimestamp(self.__version_timestamp).strftime("%Y-%m-%d")

        return None
