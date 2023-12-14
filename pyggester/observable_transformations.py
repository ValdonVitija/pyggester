from _ast import Assign, Module
import ast
import astor
from typing import Any, Tuple
from pyggester.module_importer import add_imports
from pyggester.wrappers import apply_wrappers, get_wrappers_as_strings


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

    # def visit_Assign(self, node: Assign) -> Any:
    #     print(ast.dump(node, indent=4))
    #     """
    #     Each declared collection/structure in python is represented into an Assign node, therefore
    #     we visit each Assign node and we find every observable so that we can collect them.
    #     """
    #     if isinstance(node.value, ast.Call):
    #         if getattr(node.value, "func") and getattr(node.value.func, "id"):
    #             print("INSIDE CONDITIONNNNNNNNNNNNN")
    #             if "Observable" in node.value.func.id:
    #                 append_to_list_code = (
    #                     f"""OBSERVABLE_COLLECTOR.append({node.targets[0].id})"""
    #                 )
    #                 return [node, ast.parse(append_to_list_code)]
    #     return node

    def visit_Assign(self, node: ast.Assign) -> Any:
        """
        Visit each Assign node to find and collect instances of observable types,
        indicated by 'Observable' being part of the function name.
        """
        if isinstance(node.value, ast.Call):
            func_node = node.value.func
            func_name = ""

            if isinstance(func_node, ast.Name):
                func_name = func_node.id
            elif isinstance(func_node, ast.Attribute):
                func_name = func_node.attr

            if "Observable" in func_name:
                append_to_list_code = (
                    f"OBSERVABLE_COLLECTOR.append({node.targets[0].id})"
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
    # print("after imports")
    tree = add_imports(tree, "pyggester.observable_collector", ["OBSERVABLE_COLLECTOR"])
    # print("after imports")
    tree = apply_wrappers(tree)
    # print("after apply wrappers")
    tree = apply_observable_collector_modifications(tree, run_observables)
    # print("after apply_observable_collector_modifications")

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

    transformer_appender = ObservableCollectorAppender()
    transformer_appender_tree = transformer_appender.visit(tree)
    if run_observables:
        transformer_runner = ObservableRunner()
        transformer_runner_tree = transformer_runner.visit(transformer_appender_tree)
        return transformer_runner_tree

    return transformer_appender_tree
