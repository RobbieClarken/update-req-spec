import pytest

from repin.repin import RequirementUpdater


@pytest.mark.parametrize(
    "init, final",
    [
        ("app-xyz", "app-xyz<4"),
        ("app-xyz>1.2", "app-xyz>1.2,<4"),
        ("app-xyz>=1.2", "app-xyz>=1.2,<4"),
        ("app-xyz<1.2", "app-xyz<4"),
        ("app-xyz~=1.2", "app-xyz>=1.2,<4"),
    ],
)
def test_requirement_updater(init, final):
    mock_latest_version_finder = lambda requirement: "3.4"  # noqa
    assert RequirementUpdater(init, mock_latest_version_finder).update() == final
