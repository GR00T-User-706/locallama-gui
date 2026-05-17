"""Syntax highlighter for Ollama Modelfile format."""

import re
from PySide6.QtGui import QSyntaxHighlighter, QTextCharFormat, QColor, QFont


class ModelfileHighlighter(QSyntaxHighlighter):
    """Highlights Modelfile syntax in a QTextDocument."""

    def __init__(self, document):
        super().__init__(document)
        self._rules = []
        self._build_rules()

    def _fmt(self, color: str, bold: bool = False, italic: bool = False) -> QTextCharFormat:
        fmt = QTextCharFormat()
        fmt.setForeground(QColor(color))
        if bold:
            fmt.setFontWeight(QFont.Weight.Bold)
        if italic:
            fmt.setFontItalic(True)
        return fmt

    def _build_rules(self):
        # Directives (keywords)
        directive_fmt = self._fmt("#89b4fa", bold=True)
        directives = [
            "FROM", "SYSTEM", "TEMPLATE", "PARAMETER", "ADAPTER",
            "MESSAGE", "LICENSE",
        ]
        for kw in directives:
            self._rules.append((re.compile(rf"^\s*{kw}\b", re.MULTILINE), directive_fmt))

        # String literals (double-quoted or triple-quoted)
        self._rules.append((re.compile(r'""".*?"""', re.DOTALL),
                             self._fmt("#a6e3a1")))
        self._rules.append((re.compile(r'"(?:[^"\\]|\\.)*"'),
                             self._fmt("#a6e3a1")))

        # Numbers
        self._rules.append((re.compile(r"\b\d+\.?\d*\b"),
                             self._fmt("#fab387")))

        # Parameter names (word after PARAMETER keyword)
        self._rules.append((re.compile(r"(?<=PARAMETER\s)\w+"),
                             self._fmt("#f38ba8")))

        # Comments
        self._rules.append((re.compile(r"#[^\n]*"),
                             self._fmt("#6c7086", italic=True)))

        # Role values for MESSAGE
        for role in ("user", "assistant", "system", "tool"):
            self._rules.append((re.compile(rf"\b{role}\b"),
                                 self._fmt("#cba6f7")))

        # Template variables {{ .System }} {{ .Prompt }}
        self._rules.append((re.compile(r"\{\{.*?\}\}"),
                             self._fmt("#f9e2af")))

    def highlightBlock(self, text: str):
        for pattern, fmt in self._rules:
            for match in pattern.finditer(text):
                self.setFormat(match.start(), match.end() - match.start(), fmt)
