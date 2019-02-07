import ast
from pathlib import Path

import pkg_resources
from piptools.repositories.pypi import PyPIRepository
from piptools.scripts.compile import get_pip_command


def repin_file(filename, config):
    path = Path(filename)
    source = path.read_text()
    node_finder = InstallRequiresNodeFinder()
    node_finder.visit(ast.parse(source))
    if node_finder.node is None:
        raise RuntimeError("could not find install_requires keyword")
    latest_version_finder = PipToolsLatestVersionFinder(config)
    for node in reversed(node_finder.node.value.elts):
        new_text = RequirementUpdater(node.s, latest_version_finder).update()
        source = SourceReplacer(source, node).replace_with(new_text)
    path.write_text(source)


class Config:
    def __init__(self, *, cli_options={}):
        self.cli_options = cli_options


class RequirementUpdater:
    def __init__(self, requirement, latest_version_finder):
        self._requirement = list(pkg_resources.parse_requirements(requirement))[0]
        self._find_latest_version = latest_version_finder

    @property
    def _package_name(self):
        return self._requirement.name

    def update(self):
        major_version = self._find_latest_version(self._requirement).split(".")[0]
        next_major_version = int(major_version) + 1
        spec = f"{self._minimum_version_spec},<{next_major_version}".lstrip(",")
        return f"{self._package_name}{spec}"

    @property
    def _minimum_version_spec(self):
        for op, version in self._requirement.specs:
            if op in (">", ">="):
                return f"{op}{version}"
            elif op == "~=":
                return f">={version}"
        return ""


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
        return sorted(candidates, key=lambda c: c.version)[-1].version.base_version


class SourceReplacer:
    def __init__(self, source, node):
        self._source = source
        self._node = node

    def replace_with(self, new_text):
        return self._text_before + new_text + self._text_after

    @property
    def _text_before(self):
        lines = self._source.splitlines()[: self._node.lineno]
        lines[-1] = lines[-1][: self._node.col_offset + 1]
        return "\n".join(lines)

    @property
    def _text_after(self):
        lines = self._source.splitlines()[self._node.lineno - 1 :]
        lines[0] = lines[0][self._node.col_offset + 1 + len(self._node.s) :]
        return "\n".join(lines)


class InstallRequiresNodeFinder(ast.NodeVisitor):
    node = None

    def visit_keyword(self, node):
        if node.arg == "install_requires":
            self.node = node
