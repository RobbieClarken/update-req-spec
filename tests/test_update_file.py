from textwrap import dedent

import pytest

from updatereqspec import exceptions
from updatereqspec.config import Config
from updatereqspec.update import update_file


def test_updatereqspec_raises_runtime_error_if_cant_find_install_requires(tmp_path):
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
    with pytest.raises(exceptions.InvalidSetupFile) as exc_info:
        update_file(str(setup_file), Config())
    assert "could not locate install_requires keyword in file" in str(exc_info.value)


def test_updatereqspec(tmp_path):
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
    update_file(str(setup_file), Config())
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


def test_updatereqspec_when_requirements_on_same_line(tmp_path):
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
    update_file(str(setup_file), Config())
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


def test_updatereqspec_raises_PackageNotFound_exception(tmp_path):
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
        update_file(str(setup_file), Config())
    assert "could not find a package named afdsknwfsda" in str(exc_info.value)
