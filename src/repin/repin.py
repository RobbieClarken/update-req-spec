import ast
from pathlib import Path


def repin_file(filename):
    path = Path(filename)
    source = path.read_text()
    node_finder = InstallRequiresNodeFinder()
    node_finder.visit(ast.parse(source))
    if node_finder.node is None:
        raise RuntimeError("could not find install_requires keyword")


class InstallRequiresNodeFinder(ast.NodeVisitor):
    node = None

    def visit_keyword(self, node):
        if node.arg == "install_requires":
            self.node = node
