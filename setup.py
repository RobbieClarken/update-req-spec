import re

from setuptools import setup


with open("src/updatereqspec/__init__.py") as file:
    version = re.search(r'__version__ = "(.*)"', file.read()).group(1)


setup(
    name="update-req-spec",
    version=version,
    license="MIT",
    author="Robbie Clarken",
    author_email="robert.clarken@reece.com.au",
    package_dir={"": "src"},
    packages=["updatereqspec"],
    install_requires=["click", "pip-tools"],
    entry_points={"console_scripts": ["update-req-spec=updatereqspec.cli:main"]},
)
