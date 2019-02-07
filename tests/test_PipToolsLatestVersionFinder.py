from repin.repin import Config, PipToolsLatestVersionFinder


def test_PipToolsLatestVersionFinder_uses_index_url(mocker):
    config = Config(cli_options={"--index-url": "http://index.test/"})
    finder = PipToolsLatestVersionFinder(config)
    assert finder._pip_args == ["--index-url", "http://index.test/"]