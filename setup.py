from setuptools import find_packages, setup

description = """

"""
long_description = (
    description
    + """

"""
)

setup(
    name="pyhist",
    version="0.0.1",
    author="Javier Guzman",
    author_email="jguzmanfd@gmail.com",
    description=description,
    long_description=long_description,
    packages=find_packages(),
    entry_points={"console_scripts": ["pyhist = pyhist.cli:main"]},
    install_requires=["click==7.1.2", "GitPython==3.1.1",],
    extras_require={"tests": ["black==19.10b0", "pre-commit==2.5.1", "pytest==5.4.2",]},
    url="https://github.com/jgoodman8/pyhist",
)
