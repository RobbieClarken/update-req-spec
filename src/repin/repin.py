import ast
from pathlib import Path


def repin_file(filename):
    path = Path(filename)
    source = path.read_text()
    node_finder = InstallRequiresNodeFinder()
    node_finder.visit(ast.parse(source))
    if node_finder.node is None:
        raise RuntimeError("could not find install_requires keyword")
    for node in reversed(node_finder.node.value.elts):
        new_text = (
            "channelarchiver>=0.1.0,<2" if node.s.startswith("c") else "ttmltosrt>0.5,<2"
        )
        source = SourceReplacer(source, node).replace_with(new_text)
    path.write_text(source)


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
