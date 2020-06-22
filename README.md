<p align="center">
    <br>
    <a href="https://github.com/jgoodman8/pyhist">
        <img src="https://raw.githubusercontent.com/jgoodman8/pyhist/master/assets/pyhist.png" alt="PyHist Logo" width="450"/>
    </a>
    <br>
<p>

<p align="center">
    <a href="https://pypi.python.org/pypi/pyhist/">
        <img alt="PyPi" src="https://img.shields.io/pypi/v/pyhist.svg?style=flat-square">
    </a>
    <a href="https://github.com/jgoodman8/pyhist/blob/master/LICENSE">
        <img alt="License" src="https://img.shields.io/github/license/jgoodman8/pyhist.svg?style=flat-square">
    </a>
</p>

<h3 align="center">
    <b>A Python utility to automagically update the package version from the git history and generate the Changelog</b>
</h3>


# Overview

Pyhist is a Python utility to automagically update the package version from the git history and generate the Changelog. Inspired by the [Conventional Commits](https://www.conventionalcommits.org/) specification, this tool inspects the commits history and calculates the new version.

## First steps

- **Init**: initializes the pyhist from the current git history and creates a `.pyhist` binary file and creates a 
versioning commit with the initialization of the utility.

```bash
pyhist --init
```

- **Update**: triggers the version update (minor and/or patch). The command inspects the changes applied to the git history from the previous version update and performs the following changes:
    1. Updates the version in the `setup.py`
    2. Generates a `Changelog.md` with the content of the version updates (or appends the changes if previously created)
    3. Updates the .pyhist
    4. Adds a versioning commit with the changes (i.e. `versioning: Set version to 1.3.7`)

```bash
pyhist --update
```

- **Major**: triggers the version update in the major version. This command performs the equivalent steps to the update command.

```bash
pyhist --major
```

# Installation

> Pyhist requires **Python 3.7** or higher.

## From PyPI

```bash
pip install pyhist
```

## From the source code

```bash
git clone https://github.com/jgoodman8/pyhist.git
cd pyhist
pip install -e .
```

# Tests

```bash
git clone https://github.com/jgoodman8/pyhist.git
cd pyhist
pip install -e .
pip install -e .[tests]

pytest pyhist/tests
```

# Commits specification

This project is inspired by the [Conventional Commits](https://www.conventionalcommits.org/) specification. Given this, we establish the following rules.

- Major update:
    - Explicitly called using the `pyhist --major` command.
- Minor update:
    - `feat`
- Patch update:
    - `fix`
    - `docs`
    - `test`
    - `chore`
    - `perf`
    - `refactor`
    - `style`
