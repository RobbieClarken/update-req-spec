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
        return "\n".join(lines) + "\n"
