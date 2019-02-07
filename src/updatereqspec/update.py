import ast
from pathlib import Path

from .exceptions import InvalidSetupFile
from .latest_version_finder import PipToolsLatestVersionFinder
from .requirement_updater import RequirementUpdater
from .source_replacer import SourceReplacer


def update_file(filename, config):
    path = Path(filename)
    source = path.read_text()
    latest_version_finder = PipToolsLatestVersionFinder(config)
    for node in reversed(_get_requirements_nodes(source)):
        new_requirement = RequirementUpdater(node.s, latest_version_finder).update()
        source = SourceReplacer(source, node).replace_with(new_requirement)
    path.write_text(source)


def _get_requirements_nodes(source):
    node_finder = InstallRequiresNodeFinder()
    node_finder.visit(ast.parse(source))
    if node_finder.node is None:
        raise InvalidSetupFile("could not locate install_requires keyword in file")
    return node_finder.node.value.elts


class InstallRequiresNodeFinder(ast.NodeVisitor):
    node = None

    def visit_keyword(self, node):
        if node.arg == "install_requires":
            self.node = node
