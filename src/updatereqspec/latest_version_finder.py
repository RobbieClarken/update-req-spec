from piptools.repositories.pypi import PyPIRepository
from piptools.scripts.compile import get_pip_command

from .exceptions import PackageNotFound


class PipToolsLatestVersionFinder:
    def __init__(self, config):
        self._config = config

    @property
    def _pip_args(self):
        try:
            return ["--index-url", self._config.cli_options["--index-url"]]
        except KeyError:
            return []

    def __call__(self, requirement):
        pip_command = get_pip_command()
        pip_options, _ = pip_command.parse_args(self._pip_args)
        session = pip_command._build_session(pip_options)
        repo = PyPIRepository(pip_options, session)
        candidates = repo.find_all_candidates(requirement.name)
        if len(candidates) == 0:
            raise PackageNotFound(f"could not find a package named {requirement.name}")
        return sorted(candidates, key=lambda c: c.version)[-1].version.base_version
