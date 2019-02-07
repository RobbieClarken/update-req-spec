from updatereqspec.config import Config
from updatereqspec.latest_version_finder import PipToolsLatestVersionFinder


def test_PipToolsLatestVersionFinder_uses_index_url():
    config = Config(cli_options={"--index-url": "http://index.test/"})
    finder = PipToolsLatestVersionFinder(config)
    assert finder._pip_args == ["--index-url", "http://index.test/"]
