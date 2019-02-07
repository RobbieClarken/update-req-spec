from textwrap import dedent

import pytest

from repin import repin_file


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
        repin_file(str(setup_file))
    assert "could not find install_requires keyword" in str(exc_info.value)
