import ast
import colorama
from colorama import Fore


def suggest_refactor(code):
    tree = ast.parse(code)
    suggestions = []
    for node in ast.walk(tree):
        if isinstance(node, ast.For):
            if (isinstance(node.iter, ast.Call) and
                isinstance(node.iter.func, ast.Name) and
                node.iter.func.id == "range" and
                len(node.iter.args) == 1 and
                isinstance(node.iter.args[0], ast.Call) and
                isinstance(node.iter.args[0].func, ast.Name) and
                node.iter.args[0].func.id == "len"):
                line_number = node.lineno
                line_ = f"{Fore.WHITE} Line: {Fore.GREEN} {line_number} {Fore.WHITE} | {Fore.RED} Consider using 'enumerate' instead of 'range(len())'"
                print(line_)


        if isinstance(node, ast.Assign):
            if (isinstance(node.value, ast.BinOp) and
                isinstance(node.value.op, ast.Add) and
                isinstance(node.value.left, ast.Name) and
                isinstance(node.value.right, ast.Num) and
                node.value.right.n == 1 and
                node.value.left.id == node.targets[0].id):
                line_number = node.lineno
                line_ = f"{Fore.WHITE} Line: {Fore.GREEN} {line_number} {Fore.WHITE} | {Fore.RED} Consider using the shorthand '{node.targets[0].id} += 1' instead of '{node.value.left.id} = {node.value.left.id} + 1'"
                print(line_)

            if (isinstance(node.value, ast.BinOp) and
                isinstance(node.value.op, ast.Sub) and
                isinstance(node.value.left, ast.Name) and
                isinstance(node.value.right, ast.Num) and
                node.value.right.n == 1 and
                node.value.left.id == node.targets[0].id):
                line_number = node.lineno
        if isinstance(node, ast.BinOp):
            if (isinstance(node.op, ast.Add) and
                    isinstance(node.left, ast.Str) and
                    isinstance(node.right, ast.Str)):
                    line_number = node.lineno

        indent_level = 0
        if isinstance(node, ast.If):
            indent_level += 1
            if indent_level > 4:
                    line_number = node.lineno
                    suggestions.append((line_number, "Refactor if/else chain into a switch statement or a separate method"))
                    break
        elif isinstance(node, ast.IfExp):
                indent_level -= 1

        if isinstance(node, ast.Assign):
            if isinstance(node.value, ast.Call):
                if isinstance(node.value.func, ast.Name):
                    if node.value.func.id == 'open':
                        line_number = node.lineno
                        line_ = f"{Fore.WHITE} Line: {Fore.GREEN} {line_number} {Fore.WHITE} | {Fore.RED} Consider using the context manager 'with open' instead of just 'open' for file handling"
                        print(line_)

        if isinstance(node, ast.FunctionDef):
            if len(node.body) > 20:
                is_assign = all(isinstance(stmt, ast.Assign) for stmt in node.body)
                if not is_assign:
                    pass

        if isinstance(node, ast.FunctionDef):
            num_args = len(node.args.args)
            if num_args > 4:
                line_number = node.lineno
                line_ = f"{Fore.WHITE} Line: {Fore.GREEN} {line_number} {Fore.WHITE} | {Fore.RED} To many function parameters. Consider using keyword arguments or a data object to improve readability and maintainability"

                print(line_)

        if isinstance(node, ast.For):
            has_lookup = False
            for inner_node in node.body:
                if isinstance(inner_node, ast.Compare):
                    if len(inner_node.ops) == 1 and isinstance(inner_node.ops[0], ast.In):
                        has_lookup = True
                        break

            if has_lookup:
                line_number = node.lineno
                suggestions.append((line_number, "Consider using a hash table (such as a dict) for efficient lookups"))
        

    return suggestions

code = """
for i in range(len(list)):
    print(list[i])

x = 0
y = 0
x_aaa = x_aaa + 1
y_bbbs = y_bbbs - 1
list = [1, 2, 3, 4, 5]

with open("file.txt","r") as f_stream:
    pass
f = open("file.txt", "r")
    
input = 5
if input == 1:
    print("Input is 1")
elif input == 2:
    print("Input is 2") 
elif input == 3:
    print("Input is 3")
elif input == 4:
    print("Input is 4")
elif input == 5:
    print("Input is 5")
elif input == 6:
    print("Input is 5")
else:
    print("Input is not recognized")

def func1(a1,a2,a4,a5,a6,a7):
    pass


"""

suggestions = suggest_refactor(code)
for suggestion in suggestions:
    line_number, text = suggestion
    print(f"Line {line_number}: {text}")

