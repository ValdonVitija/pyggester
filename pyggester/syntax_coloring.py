#pylint:disable=E0611
from pygments import highlight
from pygments.lexers import PythonLexer
from pygments.formatters import TerminalFormatter

class SyntaxHighlighter:
    def __init__(self):
        self.lexer = PythonLexer()
        self.formatter = TerminalFormatter()

    def highlight(self, code):
        return highlight(code, self.lexer, self.formatter)

    def print_(self, line_nr,code):
        print(f"{line_nr} | {self.highlight(code)}")



