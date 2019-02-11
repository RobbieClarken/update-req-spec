# update-req-spec

[![Build Status](https://travis-ci.org/RobbieClarken/update-req-spec.svg?branch=master)](https://travis-ci.org/RobbieClarken/update-req-spec)
[![License: MIT](https://img.shields.io/badge/license-MIT-blue.svg)](https://github.com/RobbieClarken/update-req-spec/blob/master/LICENSE)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/ambv/black)

Update Python requirements in a setup.py file to permit latest available versions.

## Motivation

You wish to cap the versions of the dependencies in your library to the major versions
that are currently released since you have tested your library against these versions and, given
everyone follows semantic versioning, minor updates should remain compatible. But keeping these
version ranges up to date with new major releases can be tedious.

`update-req-spec` makes this a little easier by updating the `install_requirements` in your
`setup.py` so that the version specifications allow the latest major releases while retaining the
minimum permitted versions. Then all you need to do is run your tests and publish a new release.

For example, given:

```python
from setuptools import setup

setup(
    # --- snip ---
    install_requires=[
        "requests",
        "Click>=6.1",
        "attrs~=18.1",
    ],
    # --- snip ---
)
```

will be transformed to:

```python
from setuptools import setup

setup(
    # --- snip ---
    install_requires=[
        "requests<3",
        "Click>=6.1,<8",
        "attrs>=18.1,<19",
    ],
    # --- snip ---
)
```

## Installation

Install with [pipsi](https://github.com/mitsuhiko/pipsi):

```bash
pipsi install update-req-sepc
```

or with pip:

```bash
python3 -m pip install update-req-spec
```

## Usage

```bash
update-req-spec setup.py
```

If you use a private packge repository:

```bash
update-req-spec --index-url http://private-repo.example/ setup.py

# or

export PIP_INDEX_URL=http://private-repo.example/
update-req-spec setup.py
```
