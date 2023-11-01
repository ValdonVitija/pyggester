import ast
from collections import defaultdict
from pyggester.syntax_coloring import SyntaxHighlighter
import array


class CodeSuggester:
    def __init__(self):
        self.highlighter = SyntaxHighlighter()
        self.handlers = [
            self.enumerate_instead_of_range_len,
            self.shorthand_arithmetic,
            self.context_managers,
            self.possitive_check_instead_of_negative_check,
            self.suggest_logging,
            self.use_dict_comprehension_instead_of_for_loop,
            self.use_str_join,
            self.suggest_list_comprehension,
        ]

    def suggest_refactor(self, file_):
        tree = ast.parse(self.fetch_file_content(file_))
        self.analyze_ast(tree)

    def fetch_file_content(self, file_):
        with open(file_, "r", encoding="UTF-8") as f_stream:
            return f_stream.read()

    def analyze_ast(self, tree):
        for node in ast.walk(tree):
            for handler in self.handlers:
                handler(node)

    # TODO : rethink about the following... not general at all, not functional!
    def function_suggestions(self, node):
        """add code here for refactoring suggestions related functions, but abstract them into separate methods"""
        if isinstance(node, ast.FunctionDef):
            if len(node.body) > 20:
                is_assign = all(isinstance(stmt, ast.Assign) for stmt in node.body)
                if not is_assign:
                    pass

        if isinstance(node, ast.FunctionDef):
            num_args = len(node.args.args)
            if num_args > 4:
                self.highlighter.print_(
                    node.lineno,
                    f"To many function paramters. Consider using keyword arguments or a data object to improve readability and maintainability",
                )

    def context_managers(self, node):
        """add code here for other refactoring suggestions related to context_managers"""
        if isinstance(node, ast.Assign):
            if isinstance(node.value, ast.Call):
                if isinstance(node.value.func, ast.Name):
                    if node.value.func.id == "open":
                        self.highlighter.print_(
                            node.lineno,
                            f"Consider using the context manager 'with open()' instead of just 'open' for file handling",
                        )

    def shorthand_arithmetic(self, node):
        if isinstance(node, ast.Assign):
            if (
                isinstance(node.value, ast.BinOp)
                and isinstance(node.value.left, ast.Name)
                and isinstance(node.value.right, ast.Num)
                and node.value.left.id == node.targets[0].id
            ):
                if isinstance(node.value.op, ast.Add):
                    if node.value.right.n == 1:
                        self.highlighter.print_(
                            node.lineno,
                            f"Consider using the shorthand '{node.targets[0].id} += 1' instead of '{node.value.left.id} = {node.value.left.id} + 1'",
                        )
                elif isinstance(node.value.op, ast.Sub):
                    if node.value.right.n == 1:
                        self.highlighter.print_(
                            node.lineno,
                            f"Consider using the shorthand '{node.targets[0].id} -= 1' instead of '{node.value.left.id} = {node.value.left.id} - 1'",
                        )
                elif isinstance(node.value.op, ast.Mult):
                    if node.value.right.n == 1:
                        self.highlighter.print_(
                            node.lineno,
                            f"Consider using the shorthand '{node.targets[0].id} *= 1' instead of '{node.value.left.id} = {node.value.left.id} * 1'",
                        )
                elif isinstance(node.value.op, ast.Div):
                    if node.value.right.n == 1:
                        self.highlighter.print_(
                            node.lineno,
                            f"Consider using the shorthand '{node.targets[0].id} /= 1' instead of '{node.value.left.id} = {node.value.left.id} / 1'",
                        )
                elif isinstance(node.value.op, ast.Mod):
                    if node.value.right.n == 1:
                        self.highlighter.print_(
                            node.lineno,
                            f"Consider using the shorthand '{node.targets[0].id} %= 1' instead of '{node.value.left.id} = {node.value.left.id} % 1'",
                        )

    def enumerate_instead_of_range_len(self, node):
        if isinstance(node, ast.For):
            if (
                isinstance(node.iter, ast.Call)
                and isinstance(node.iter.func, ast.Name)
                and node.iter.func.id == "range"
                and len(node.iter.args) == 1
                and isinstance(node.iter.args[0], ast.Call)
                and isinstance(node.iter.args[0].func, ast.Name)
                and node.iter.args[0].func.id == "len"
            ):
                self.highlighter.print_(
                    node.lineno, "Consider using 'enumerate' instead of 'range(len())'"
                )

    def suggest_list_comprehension(self, node):
        if self.is_for_loop_with_append(node):
            self.highlighter.print_(
                node.lineno,
                "Consider using a list comprehension instead of a for loop with '.append'",
            )

    def is_for_loop_with_append(self, node):
        return (
            isinstance(node, ast.For)
            and self.is_valid_target(node.target)
            and self.is_valid_body(node.body)
        )

    def is_valid_target(self, target):
        return isinstance(target, ast.Name)

    def is_valid_body(self, body):
        if len(body) == 1 and isinstance(body[0], ast.Expr):
            call = body[0].value
            return isinstance(call, ast.Call) and self.is_append_call(call)
        return False

    def is_append_call(self, call):
        return (
            isinstance(call.func, ast.Attribute)
            and isinstance(call.func.value, ast.Name)
            and call.func.attr == "append"
        )

    def suggest_zip_refactoring(self, node):
        if isinstance(node, ast.For):
            if any(
                isinstance(inner, ast.Call) and inner.func.id == "zip"
                for inner in node.body
            ):
                return []
            self.highlighter.print_(
                node.lineno,
                f"Consider using `zip` to iterate over multiple sequences in parallel",
            )

    def possitive_check_instead_of_negative_check(self, node):
        if (
            isinstance(node, ast.If)
            and isinstance(node.body[0], ast.Pass)
            and isinstance(node.test, ast.Name)
        ):
            self.highlighter.print_(
                node.lineno,
                f"Consider using 'if not {node.test.id}:' instead of 'if {node.test.id}: pass'",
            )



    def suggest_logging(self, node):
        if isinstance(node, ast.Try):
            use_logging = False
            for child in node.body:
                if isinstance(child, ast.Expr) and isinstance(child.value, ast.Call):
                    func_name = (
                        child.value.func.attr
                        if isinstance(child.value.func, ast.Attribute)
                        else None
                    )
                    if func_name in ["debug", "info", "warning", "error"]:
                        use_logging = True
                        break
            if not use_logging:
                self.highlighter.print_(
                    node.lineno,
                    "Consider using logging to log any messages or errors caught in the except block.",
                )

 

    def use_dict_comprehension_instead_of_for_loop(self, node):
        if isinstance(node, ast.For):
            if self.is_dict_assignment(node):
                self.highlighter.print_(
                    node.lineno,
                    "Consider using a dictionary comprehension instead of a for loop with assignment",
                )

    def is_dict_assignment(self, node):
        if (
            isinstance(node.body[0], ast.Assign)
            and isinstance(node.body[0].targets[0], ast.Subscript)
            and isinstance(node.body[0].targets[0].value, ast.Name)
        ):
            return True
        return False


    def use_str_join(self, node):
        def is_string_concatenation(node):
            return (
                isinstance(node, ast.BinOp)
                and isinstance(node.op, ast.Add)
                and (isinstance(node.left, ast.Str) or isinstance(node.right, ast.Str))
            )

        def is_string_concatenation_in_aug_assign(node):
            return (
                isinstance(node, ast.AugAssign)
                and isinstance(node.op, ast.Add)
                and isinstance(node.target, ast.Name)
                and isinstance(node.value, ast.Str)
            )

        if is_string_concatenation(node) or is_string_concatenation_in_aug_assign(node):
            self.highlighter.print_(
                node.lineno,
                "Consider using 'str.join()' method instead of concatenating strings with '+' or '+='",
            )
