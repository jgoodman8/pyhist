from dataclasses import dataclass
from typing import Optional

from git import Commit

from pyhist.versioning.version import Version


@dataclass
class PyHistItem:
    commit: Optional[Commit]
    version: Optional[Version]
    is_version: bool
