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

__all__ = ["suggest_refactor"]


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
        use_list_comprehension_instead_of_for_loop(node, highlighter)
        possitive_check_instead_of_negative_check(node, highlighter)
        redundant_parentheses(node, highlighter)
        filter_instead_of_looping_with_condition(node, highlighter)
        suggest_logging(node, highlighter)



def function_suggestions(node, highlighter):
    """add code here for refactoring suggestions related functions, but abstract them into separate methods"""
    if isinstance(node, ast.FunctionDef):
        if len(node.body) > 20:
            is_assign = all(isinstance(stmt, ast.Assign) for stmt in node.body)
            if not is_assign:
                pass

    if isinstance(node, ast.FunctionDef):
        num_args = len(node.args.args)
        if num_args > 4:
            highlighter.print_(node.lineno, f"To many function paramters. Consider using keyword arguments or a data object to improve readability and maintainability")

def context_managers(node, highlighter):
    """add code here for other refactoring suggestions related to context_managers"""
    if isinstance(node, ast.Assign):
        if isinstance(node.value, ast.Call):
            if isinstance(node.value.func, ast.Name):
                if node.value.func.id == 'open':
                    highlighter.print_(node.lineno, f"Consider using the context manager 'with open()' instead of just 'open' for file handling")

def shorthand_arithmetic(node, highlighter):
    if isinstance(node, ast.Assign):
        if (isinstance(node.value, ast.BinOp) and
        isinstance(node.value.left, ast.Name) and
        isinstance(node.value.right, ast.Num) and
        node.value.left.id == node.targets[0].id):
            if isinstance(node.value.op, ast.Add):
                if node.value.right.n == 1:
                    highlighter.print_(node.lineno, f"Consider using the shorthand '{node.targets[0].id} += 1' instead of '{node.value.left.id} = {node.value.left.id} + 1'")
            elif isinstance(node.value.op, ast.Sub):
                if node.value.right.n == 1:
                    highlighter.print_(node.lineno, f"Consider using the shorthand '{node.targets[0].id} -= 1' instead of '{node.value.left.id} = {node.value.left.id} - 1'")
            elif isinstance(node.value.op, ast.Mult):
                if node.value.right.n == 1:
                    highlighter.print_(node.lineno, f"Consider using the shorthand '{node.targets[0].id} *= 1' instead of '{node.value.left.id} = {node.value.left.id} * 1'")
            elif isinstance(node.value.op, ast.Div):
                if node.value.right.n == 1:
                    highlighter.print_(node.lineno, f"Consider using the shorthand '{node.targets[0].id} /= 1' instead of '{node.value.left.id} = {node.value.left.id} / 1'")
            elif isinstance(node.value.op, ast.Mod):
                if node.value.right.n == 1:
                    highlighter.print_(node.lineno, f"Consider using the shorthand '{node.targets[0].id} %= 1' instead of '{node.value.left.id} = {node.value.left.id} % 1'")


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



def use_list_comprehension_instead_of_for_loop(node, highlighter):
    if isinstance(node, ast.For):
        if (len(node.body) == 1 and
            isinstance(node.body[0], ast.AugAssign) and
            isinstance(node.body[0].target, ast.Name) and
            node.body[0].target.id == "result" and
            isinstance(node.body[0].value, ast.BinOp) and
            node.body[0].op == ast.Add and
            isinstance(node.body[0].value.left, ast.Name) and
            node.body[0].value.left.id == "result" and
            isinstance(node.body[0].value.right, ast.Name)):
            highlighter.print_(node.lineno, "Consider using a list comprehension instead of a for loop with '.append'")


def suggest_zip_refactoring(node, highlighter):
    if isinstance(node, ast.For):
        if any(isinstance(inner, ast.Call) and inner.func.id == 'zip' for inner in node.body):
            return []
        highlighter.print_(node.lineno, f"Consider using `zip` to iterate over multiple sequences in parallel")
        

def possitive_check_instead_of_negative_check(node, highlighter):
    if (isinstance(node, ast.If) and
        isinstance(node.body[0], ast.Pass) and
        isinstance(node.test, ast.Name)):
        highlighter.print_(node.lineno, f"Consider using 'if not {node.test.id}:' instead of 'if {node.test.id}: pass'")


def redundant_parentheses(node, highlighter):
    if (isinstance(node, ast.BinOp) and
        isinstance(node.left, ast.BinOp) and
        isinstance(node.right, ast.BinOp)):
        highlighter.print_(node.lineno, "Consider removing redundant parentheses in expression")

def filter_instead_of_looping_with_condition(node, highlighter):
    if (isinstance(node, ast.For) and
        isinstance(node.target, ast.Name) and
        isinstance(node.iter, ast.Call) and
        isinstance(node.body[0], ast.If) and
        isinstance(node.body[0].test, ast.Compare)):
        highlighter.print_(node.lineno, "Consider using 'filter()' instead of a loop for a more concise code")


# def suggest_logging(node, highlighter):
#     if isinstance(node, ast.Try):
#         use_logging = False
#         for child in node.body:
#             if isinstance(child, ast.Expr) and isinstance(child.value, ast.Call) and child.value.func.id.startswith("logging."):
#                 use_logging = True
#                 break
#         if not use_logging:
#             highlighter.print_(node.lineno, "Consider using logging to log any messages or errors caught in the except block.")



def suggest_logging(node, highlighter):
    if isinstance(node, ast.Try):
        use_logging = False
        for child in node.body:
            if isinstance(child, ast.Expr) and isinstance(child.value, ast.Call):
                func_name = child.value.func.attr if isinstance(child.value.func, ast.Attribute) else None
                if func_name in ['debug', 'info', 'warning', 'error']:
                    use_logging = True
                    break
        if not use_logging:
            highlighter.print_(node.lineno, "Consider using logging to log any messages or errors caught in the except block.")
