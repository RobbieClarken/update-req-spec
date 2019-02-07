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
def test_requirement_updater(mocker, init, final):
    mocker.patch("repin.repin._get_latest_version", return_value="3.4")
    assert RequirementUpdater(init).update() == final
