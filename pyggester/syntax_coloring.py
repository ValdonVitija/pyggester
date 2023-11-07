# """
# This module also needs to be refactored. Currently it is functional but not diverise enough.
# This needs more options on the coloring, more efficient processing...
# """
# # pylint:disable=E0611
# from pygments import highlight
# from pygments.lexers import PythonLexer
# from pygments.formatters import TerminalFormatter
# import keyword


# class SyntaxHighlighter:
#     def __init__(self):
#         self.lexer = PythonLexer()
#         self.formatter = TerminalFormatter()

#     def highlight(self, code):
#         message_words = code.split(" ")
#         full_message = ""
#         for word in message_words:
#             if (
#                 word.startswith("'")
#                 or word.endswith("'")
#                 or word.startswith('"')
#                 or word.endswith('"')
#             ):
#                 word = highlight(word, self.lexer, self.formatter)
#                 word = word.replace("\n", "")
#                 full_message += word + " "
#             else:
#                 full_message += word + " "
#         return full_message

#     def print_(self, line_nr, code):
#         print(f" {line_nr} | {self.highlight(code)}")
