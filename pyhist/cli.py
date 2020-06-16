import click

from pyhist.pyhist import PyHist
from pyhist.history import GitHistory, History
from pyhist.io.changelog_generator import ChangelogGenerator
from pyhist.io.setup_parser import SetupParser
from pyhist.versioning.semantic_versioning import SemanticVersioning


@click.command()
@click.option("--init", is_flag=True, help="")
@click.option("--update", is_flag=True, help="")
@click.option("--major", is_flag=True, help="")
def main(init: bool, update: bool, major: bool):
    git_history = GitHistory()
    history = History()
    version_parser = SetupParser()
    semantic_versioning = SemanticVersioning(git_history=git_history, history=history)
    changelog_generator = ChangelogGenerator(history=history)

    pyhist = PyHist(
        git_history=git_history,
        history=history,
        semantic_versioning=semantic_versioning,
        changelog_generator=changelog_generator,
        setup_parser=version_parser,
    )

    if init:
        pyhist.setup()
    elif update:
        pyhist.update()
    elif major:
        pyhist.major()
