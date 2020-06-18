import os


class BaseValidationTest:
    git_folder = ".git"
    history_route = ".pyhist"
    setup_file_route = "setup.py"
    file_content = """
from setuptools import setup
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
)
"""

    @classmethod
    def setup_method(cls):
        cls.setup_git()
        cls.create_setup_file()

    @classmethod
    def teardown_method(cls):
        cls.teardown_history()
        cls.teardown_git()
        cls.remove_setup_file()
        cls.clean()

    @classmethod
    def create_setup_file(cls):
        os.system(f"touch {cls.setup_file_route}")
        os.system(f'echo "{cls.file_content}" >> {cls.setup_file_route}')

    @classmethod
    def remove_setup_file(cls):
        os.system(f"rm {cls.setup_file_route}")

    @classmethod
    def teardown_history(cls):
        os.system(f"rm {cls.history_route}")

    @classmethod
    def setup_git(cls):
        os.system("git init")
        os.system('git config --global user.email "test@test.com"')
        os.system('git config --global user.name "Test"')

    @classmethod
    def teardown_git(cls):
        if os.path.exists(cls.git_folder):
            os.system(f"rm -r {cls.git_folder}")

    @classmethod
    def clean(cls):
        for file in os.listdir(os.curdir):
            if ".py" not in file:
                os.system(f"rm {file}")
