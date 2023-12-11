from _ast import Assign, Module
import ast
import astor
from typing import Any, Tuple
from pyggester.module_importer import add_imports
from pyggester.wrappers import apply_wrappers, get_wrappers_as_strings


# class ObservableCollectorDeclaration(ast.NodeTransformer):

#     """
#     This transformer handles 'three' tasks:

#     *   Firstly, it declares a list in the global scope of the module,
#         right after import statements. This list serves as a container for all observables.
#         Since standard Python collections are objects, they can be stored by reference,
#         allowing us to access all observables through a single object.
#         ----------------------------------
#         import module1
#         import module2
#         ...(other import stmts)

#         OBSERVABLE_COLLECTOR = []
#         ----------------------------------
#     """

#     __slots__: Tuple[str] = ()

#     def visit_Module(self, node):
#         """
#         Since we need to declare a list in the global/module scope
#         we start to visit from the top layer. We iteratively
#         go over each node and once we hit a node that is not related
#         to imports we immediatly declare a list there.

#         #TODO might need to refactor this if its not general enough.
#         Need to do a lot of tests on this.
#         """
#         counter = 0
#         import_index = None
#         for index, child in enumerate(ast.walk(node)):
#             if not isinstance(child, (ast.Import, ast.ImportFrom)):
#                 counter += 1
#             if counter == 1:
#                 import_index = index

#         list_declaration = ast.parse("OBSERVABLE_COLLECTOR = []").body[0]
#         node.body.insert(import_index, list_declaration)

#         return node


class ObservableCollectorAppender(ast.NodeTransformer):
    """
    * Collects each observable instance by appending it into the
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
    """

    __slots__: Tuple[str] = ()

    def visit_Assign(self, node: Assign) -> Any:
        """
        Each declared collection/structure in python is represented into an Assign node, therefore
        we visit each Assign node and we find every observable so that we can collect them.
        """
        if isinstance(node.value, ast.Call):
            if getattr(node.value, "func") and getattr(node.value.func, "id"):
                if "Observable" in node.value.func.id:
                    append_to_list_code = (
                        f"""OBSERVABLE_COLLECTOR.append({node.targets[0].id})"""
                    )
                    return [node, ast.parse(append_to_list_code)]
        return node


class ObservableRunner(ast.NodeTransformer):
    """
    *   This transformer inserts the code that runs every observable.
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

    def visit_Module(self, node: Module) -> Any:
        observable_runner_code = (
            """for observable in OBSERVABLE_COLLECTOR: observable.run()"""
        )
        observable_runner_parsed = ast.parse(observable_runner_code)
        # We don't need to index the running code of observables because
        # if we just appended, the append method take care of it.
        # It is always going to be inserted at the end of the module in global scope
        node.body.append(observable_runner_parsed)
        return node


def apply_observable_collector_transformations(
    tree: ast.AST, run_observables=False
) -> str:
    """
    Basically does anything needed for pyggester to do its analysis and returns the modified
    code. The result of this function should be stored into a new file that replicates the original
    one.
    """
    tree = add_imports(tree, "pyggester.observables", get_wrappers_as_strings())
    tree = add_imports(tree, "pyggester.observable_collector", ["OBSERVABLE_COLLECTOR"])
    tree = apply_wrappers(tree)
    tree = apply_observable_collector_modifications(tree, run_observables)
    print(tree)

    return astor.to_source(tree)


def apply_observable_collector_modifications(tree: ast.AST, run_observables) -> ast.AST:
    """
    Applying observable collector related modifications to the modules ast represenation.
    1. Declare the observable collector
    2. Append each observable into the observable collector
    3. Put the code that actually runs the collected observables.

    Since this procedure will be ran per module, it means we suggest on the go.
    If anything has been found in the module being analyzed, we will suggest on the go and then immediatly move to the next module/file
    for analysis if there are any other modules/files.
    """
    # transformer = ObservableCollectorDeclaration()
    # transformed_tree = transformer.visit(tree)

    transformer_appender = ObservableCollectorAppender()
    # transformer_appender_tree = transformer_appender.visit(transformed_tree)
    transformer_appender_tree = transformer_appender.visit(tree)

    if run_observables:
        transformer_runner = ObservableRunner()
        transformer_runner_tree = transformer_runner.visit(transformer_appender_tree)
        return transformer_runner_tree

    return transformer_appender_tree


# code = """
# import math
# import random

# list_ = [1,2]
# list_2 = [2,4,3,2,4]
# dict_1 = {}
# def some_function():
#     a = [1,1,1]

# """

# # Parse the code into an AST
# tree = ast.parse(code)
# print(apply_observable_collector_transformations(tree=tree))
