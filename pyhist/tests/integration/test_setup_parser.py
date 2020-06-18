import os

import pytest

from pyhist.io.setup_parser import SetupParser
from pyhist.versioning.version_exception import VersionException


class TestSetupParser:
    file_content = """from setuptools import setup
setup(
    name='package-name',
    version='0.0.0',
    author='Author',
    author_email='author@test.com',
    description='',
    packages=[
        'package.main',
        'package.cli',
    ],
    install_requires=[
        'package==0.0.1',
        'test-package==0.0.0',
    ],
    url='http://test.com/package',
)"""

    @pytest.fixture(scope="function")
    def setup_file(self) -> str:
        file_route = "setup.py"

        os.system(f"touch {file_route}")
        os.system(f'echo "{TestSetupParser.file_content}" >> {file_route}')

        yield file_route

        os.system(f"rm {file_route}")

    def test_get_current_version_parts_ExistsSetupWithVersion_ExtractsVersionParts(
        self, setup_file
    ):
        version_parser = SetupParser(route=setup_file)
        major, minor, patch = version_parser.get_current_version_parts()

        assert major == 0
        assert minor == 0
        assert patch == 0

    def test_get_current_version_parts_NotExistsSetupWithVersion_RaisesVersionException(
        self,
    ):
        version_parser = SetupParser(route="setup.py")

        with pytest.raises(VersionException, match="Cannot find setup.py"):
            version_parser.get_current_version_parts()

    def test_persist_current_version_ExistsSetupWithVersion_UpdatesCurrentVersion(
        self, setup_file
    ):
        # arrange
        version_parser = SetupParser(route=setup_file)
        expected_major, expected_minor, expected_patch = 2, 1, 4

        # act
        version_parser.persist_version(
            version=f"{expected_major}.{expected_minor}.{expected_patch}"
        )

        # assert
        major, minor, patch = version_parser.get_current_version_parts()
        assert major == expected_major
        assert minor == expected_minor
        assert patch == expected_patch

    def test_persist_current_version_NotExistsSetupWithVersion_RaisesVersionException(
        self,
    ):
        # arrange
        version_parser = SetupParser(route="setup.py")
        expected_major, expected_minor, expected_patch = 2, 1, 4

        # act
        with pytest.raises(VersionException, match="Cannot find setup.py"):
            version_parser.persist_version(
                version=f"{expected_major}.{expected_minor}.{expected_patch}"
            )
