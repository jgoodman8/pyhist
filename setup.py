from os import path

from setuptools import find_packages, setup

this_directory = path.abspath(path.dirname(__file__))
with open(path.join(this_directory, "README.md"), encoding="utf-8") as f:
    long_description = f.read()

setup(
    name="pyhist",
    version="0.0.4",
    author="Javier Guzman",
    author_email="jguzmanfd@gmail.com",
    long_description=long_description,
    long_description_content_type="text/markdown",
    packages=find_packages(),
    license="Apache Software License",
    entry_points={"console_scripts": ["pyhist = pyhist.cli:main"]},
    install_requires=["click==7.1.2", "GitPython==3.1.1",],
    extras_require={"tests": ["black==19.10b0", "pre-commit==2.5.1", "pytest==5.4.2",]},
    url="https://github.com/jgoodman8/pyhist",
)
