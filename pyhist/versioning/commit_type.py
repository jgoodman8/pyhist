from enum import Enum


class CommitType(Enum):
    Chore = "chore"
    Docs = "docs"
    Feature = "feat"
    Fix = "fix"
    Performance = "perf"
    Refactor = "refactor"
    Release = "release"
    Style = "style"
    Test = "test"
    Versioning = "versioning"
