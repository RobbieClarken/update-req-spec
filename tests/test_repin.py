from textwrap import dedent

import pytest

from repin import exceptions, repin_file
from repin.repin import Config


def test_repin_raises_runtime_error_if_cant_find_install_requires(tmp_path):
    setup_file = tmp_path / "setup.py"
    setup_file.write_text(
        dedent(
            """\
            from setuptools import setup
            setup(
                name="example",
                version="0.0.0",
            )
            """
        )
    )
    with pytest.raises(RuntimeError) as exc_info:
        repin_file(str(setup_file), Config())
    assert "could not find install_requires keyword" in str(exc_info.value)


def test_repin(tmp_path):
    setup_file = tmp_path / "setup.py"
    setup_file.write_text(
        dedent(
            """\
            from setuptools import setup
            setup(
                name="example",
                version="0.0.0",
                install_requires=[
                    "channelarchiver~=0.1.0",
                    "ttmltosrt>0.5",
                ],
            )
            """
        )
    )
    repin_file(str(setup_file), Config())
    expected_text = dedent(
        """\
        from setuptools import setup
        setup(
            name="example",
            version="0.0.0",
            install_requires=[
                "channelarchiver>=0.1.0,<2",
                "ttmltosrt>0.5,<2",
            ],
        )
        """
    )
    assert setup_file.read_text() == expected_text


def test_repin_when_requirements_on_same_line(tmp_path):
    setup_file = tmp_path / "setup.py"
    setup_file.write_text(
        dedent(
            """\
            from setuptools import setup
            setup(
                name="example",
                version="0.0.0",
                install_requires=[
                    "channelarchiver~=0.1.0", "ttmltosrt>0.5",
                ],
            )
            """
        )
    )
    repin_file(str(setup_file), Config())
    expected_text = dedent(
        """\
        from setuptools import setup
        setup(
            name="example",
            version="0.0.0",
            install_requires=[
                "channelarchiver>=0.1.0,<2", "ttmltosrt>0.5,<2",
            ],
        )
        """
    )
    assert setup_file.read_text() == expected_text


def test_repin_raises_PackageNotFound_exception(tmp_path):
    setup_file = tmp_path / "setup.py"
    setup_file.write_text(
        dedent(
            """\
            from setuptools import setup
            setup(
                name="example",
                version="0.0.0",
                install_requires=[
                    "afdsknwfsda",
                ],
            )
            """
        )
    )
    with pytest.raises(exceptions.PackageNotFound) as exc_info:
        repin_file(str(setup_file), Config())
    assert "afdsknwfsda not found" in str(exc_info.value)
