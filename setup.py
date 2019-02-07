import re

from setuptools import setup


with open("src/repin/__init__.py") as file:
    version = re.search(r'__version__ = "(.*)"', file.read()).group(1)


setup(
    name="re-pin",
    version=version,
    license="MIT",
    author="Robbie Clarken",
    author_email="robert.clarken@reece.com.au",
    package_dir={"": "src"},
    packages=["repin"],
    install_requires=["click", "pip-tools"],
    entry_points={"console_scripts": ["re-pin=repin.cli:main"]},
)
