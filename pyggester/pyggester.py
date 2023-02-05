#pylint:disable=E0611
import ast
import colorama
from colorama import Fore
import pathlib
from termcolor import colored
from pygments import highlight
from pygments.lexers import PythonLexer
from pygments.formatters import TerminalFormatter
from pyggester.syntax_coloring import SyntaxHighlighter


def suggest_refactor(file_):
    highlighter = SyntaxHighlighter()
    tree = ast.parse(fetch_file_content(file_))
    analyze_ast(tree, highlighter)

def fetch_file_content(file_):
    with open(file_, "r", encoding="UTF-8") as f_stream:
        return f_stream.read()

def analyze_ast(tree, highlighter):
    for node in ast.walk(tree):
        enumerate_instead_of_range_len(node, highlighter)
        shorthand_arithmetic(node, highlighter)
        context_managers(node, highlighter)
        function_suggestions(node, highlighter)

def function_suggestions(node, highlighter):
    if isinstance(node, ast.FunctionDef):
        if len(node.body) > 20:
            is_assign = all(isinstance(stmt, ast.Assign) for stmt in node.body)
            if not is_assign:
                pass

    if isinstance(node, ast.FunctionDef):
        num_args = len(node.args.args)
        if num_args > 4:
            highlighter.print_(node.lineno, f"To many function paramters. Consider using keyword arguments or a data object to improve readability and maintainability")

    if isinstance(node, ast.For):
        has_lookup = False
        for inner_node in node.body:
            if isinstance(inner_node, ast.Compare):
                if len(inner_node.ops) == 1 and isinstance(inner_node.ops[0], ast.In):
                    has_lookup = True
                    break

        if has_lookup:
            line_number = node.lineno

def context_managers(node, highlighter):
    if isinstance(node, ast.Assign):
        if isinstance(node.value, ast.Call):
            if isinstance(node.value.func, ast.Name):
                if node.value.func.id == 'open':
                    highlighter.print_(node.lineo, f"Consider using the context manager 'with open' instead of just 'open' for file handling")

def shorthand_arithmetic(node, highlighter):
    if isinstance(node, ast.Assign):
        if (isinstance(node.value, ast.BinOp) and
                isinstance(node.value.op, ast.Add) and
                isinstance(node.value.left, ast.Name) and
                isinstance(node.value.right, ast.Num) and
                node.value.right.n == 1 and
                node.value.left.id == node.targets[0].id):
                highlighter.print_(node.lineno, f"Consider using the shorthand '{node.targets[0].id} += 1' instead of '{node.value.left.id} = {node.value.left.id} + 1'")

        if (isinstance(node.value, ast.BinOp) and
                isinstance(node.value.op, ast.Sub) and
                isinstance(node.value.left, ast.Name) and
                isinstance(node.value.right, ast.Num) and
                node.value.right.n == 1 and
                node.value.left.id == node.targets[0].id):
                highlighter.print_(node.lineno, f"Consider using the shorthand '{node.targets[0].id} -= 1' instead of '{node.value.left.id} = {node.value.left.id} - 1'")

def enumerate_instead_of_range_len(node, highlighter):
    if isinstance(node, ast.For):
        if (isinstance(node.iter, ast.Call) and
                isinstance(node.iter.func, ast.Name) and
                node.iter.func.id == "range" and
                len(node.iter.args) == 1 and
                isinstance(node.iter.args[0], ast.Call) and
                isinstance(node.iter.args[0].func, ast.Name) and
                node.iter.args[0].func.id == "len"):
            highlighter.print_(node.lineno, "Consider using 'enumerate' instead of 'range(len())'")
