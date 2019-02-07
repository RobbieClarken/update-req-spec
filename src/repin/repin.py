import ast
from pathlib import Path

from .latest_version_finder import PipToolsLatestVersionFinder
from .requirement_updater import RequirementUpdater
from .source_replacer import SourceReplacer


def repin_file(filename, config):
    path = Path(filename)
    source = path.read_text()
    node_finder = InstallRequiresNodeFinder()
    node_finder.visit(ast.parse(source))
    if node_finder.node is None:
        raise RuntimeError("could not find install_requires keyword")
    latest_version_finder = PipToolsLatestVersionFinder(config)
    for node in reversed(node_finder.node.value.elts):
        new_requirement = RequirementUpdater(node.s, latest_version_finder).update()
        source = SourceReplacer(source, node).replace_with(new_requirement)
    path.write_text(source)


class InstallRequiresNodeFinder(ast.NodeVisitor):
    node = None

    def visit_keyword(self, node):
        if node.arg == "install_requires":
            self.node = node
