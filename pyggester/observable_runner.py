import ast
import astor  # You can use astor to convert the modified AST back to source code
from typing import Tuple


class ObservableCollectorTransformer(ast.NodeTransformer):

    """
    This transformer handles 'three' tasks:

    *   Firstly, it declares a list in the global scope of the module,
        right after import statements. This list serves as a container for all observables.
        Since standard Python collections are objects, they can be stored by reference,
        allowing us to access all observables through a single object.
        ----------------------------------
        import module1
        import module2
        ...(other import stmts)

        OBSERVABLE_COLLECTOR = []
        ----------------------------------
    *   Secondly, it will collect each observable instance by appending it into the
        OBSERVBALE_COLLECTOR
        ----------------------------------
        import module1
        import module2
        ...(other import stmts)

        OBSERVABLE_COLLECTOR = []
        ...(other stmts)

        list_ = ObservableList([1,2,3])
        OBSERVABLE_COLLECTOR.append(list_)
        ---------------------------------

    *   Thirdly, it inserts the code that runs every observable.
        Observables don't explicitly run themselves to print the collected suggestions,
        because they might still be in use elsewhere.
        For example, they could have been passed as function parameters.
        However, by running the observables in the global scope after everything in the module,
        we ensure that collections declared in that scope have been fully processed,
        even if they were given or injected into other modules, classes, or functions.
        -----------------------------------
        import module1
        import module2
        ...
        (functions, classes and every possible python construct)
        ...
        for observable in OBSERVABLE_COLLECTOR:
            observable.run()
        -----------------------------------
    """

    __slots__: Tuple[str] = ()

    def visit_Module(self, node):
        print(ast.dump(node, indent=4))
        import_index = None
        for i, stmt in enumerate(node.body):
            if isinstance(stmt, ast.Import) or isinstance(stmt, ast.ImportFrom):
                import_index = i
            if isinstance(stmt, ast.Assign):
                if isinstance(stmt.value, ast.Call):
                    if getattr(stmt.value, "func") and getattr(stmt.value.func, "id"):
                        if "Observable" in stmt.value.func.id:
                            append_to_list_code = f"""
OBSERVABLE_COLLECTOR.append({stmt.targets[0].id})
                            """
                            node.body.insert(i + 1, ast.parse(append_to_list_code))

        list_declaration = ast.parse("OBSERVABLE_COLLECTOR = []").body[0]
        node.body.insert(import_index + 1, list_declaration)

        observable_runner_code = """
for observable in OBSERVABLE_COLLECTOR:
    observable.run()
        """
        observable_runner_parsed = ast.parse(observable_runner_code)
        # We don't need to index the running code of observables because
        # if we just appended, the append method take care of it.
        # It is always going to be inserted at the end of the module in global scope
        node.body.append(observable_runner_parsed)
        return node


def apply_observable_collector_transformations(tree):
    # tree = ast.parse(source_code)
    transformer = ObservableCollectorTransformer()
    tree = transformer.visit(tree)

    return tree


# Your module code
code = """
import math
import random

list_ = Observable([1,2])
list_2 = ObservableList([2,4,3,2,4])
dict_1 = ObservableDict({})
def some_function():
    a = ObservableList([1,1,1])

"""

# Parse the code into an AST
tree = ast.parse(code)

# Apply the custom transformer
transformer = ObservableCollectorTransformer()
transformed_tree = transformer.visit(tree)

# You can print the modified code
modified_code = astor.to_source(transformed_tree)
print(modified_code)
