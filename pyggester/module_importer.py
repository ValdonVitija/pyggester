import ast
from typing import Any, Tuple, Set


class ImportsVisitor(ast.NodeVisitor):
    """
    AST visitor to check if a specific module or names are imported in the code.
    """

    __slots__: Tuple[str] = ("module_name", "imported", "names")

    def __init__(self, module_name: str, names: Set[str]) -> None:
        """
        Args:
            module_name (str): The name of the module to check for.
            imported (bool): Whether the module is imported or not.
            names (Set[str]): Names to check for in case of 'from import' (default is None).
        """
        self.module_name = module_name
        self.imported = False
        self.names = names

    def visit_Import(self, node: ast.Import) -> Any:
        """
        Visit an Import node.

        Check if the specified module is imported.

        Args:
            node (ast.Import): The Import node to visit.
        """
        for name in node.names:
            if name.name == self.module_name:
                self.imported = True

    def visit_ImportFrom(self, node: ast.ImportFrom) -> Any:
        """
        Visit an ImportFrom node.

        Check if the specified module is imported using 'from import'.

        Args:
            node (ast.ImportFrom): The ImportFrom node to visit.
        """
        if node.module == self.module_name:
            self.imported = True


class ImportModuleTransformer(ast.NodeTransformer):
    """AST transformer to add or update an import statement for a specific module."""

    __slots__: Tuple[str] = ("module_name", "names", "tree_", "imports_visitor")

    def __init__(
        self, tree_: ast.AST, module_name: str, names: Set[str] = None
    ) -> None:
        """
        Args:
            module_name (str): Current module being transformed.
            names (Set[str]): All ObservableWrappers needed to be imported on each module.
            tree_ (ast.AST): Abstract syntax tree of the module.
            imports_visitor (ImportsVisitor): Information fetcher for imported modules.
        """
        self.module_name = module_name
        self.names = names
        self.tree_ = tree_
        self.imports_visitor = ImportsVisitor(module_name, names)

    def visit_Module(self, node: ast.Module) -> Any:
        """
        Visit a Module node.

        Replace any existing import statement for 'pyggester.wrappers' with a new import statement.

        Args:
            node (ast.Module): The Module node to visit.

        Returns:
            ast.Module: The transformed Module node.
        """
        self.imports_visitor.visit(self.tree_)
        import_stmt = None
        if self.imports_visitor.imported:
            for node_ in ast.walk(node):
                if (
                    isinstance(node_, ast.ImportFrom)
                    and node_.module == self.module_name
                ):
                    node.body.remove(node_)

                elif isinstance(node_, ast.Import):
                    for name_ in node_.names:
                        if name_.name == self.module_name:
                            node.body.remove(node_)
            if self.names:
                import_stmt = ast.ImportFrom(
                    module=self.module_name,
                    names=[ast.alias(name=name, asname=None) for name in self.names],
                    level=0,
                )
            if import_stmt:
                node.body.insert(0, import_stmt)
        else:
            if self.names:
                import_stmt = ast.ImportFrom(
                    module=self.module_name,
                    names=[ast.alias(name=name, asname=None) for name in self.names],
                    level=0,
                )
            if import_stmt:
                node.body.insert(0, import_stmt)

        return node


def add_imports(tree: str, module_, wrappers) -> ast.AST:
    """
    Adds Wrapper imports to each module being transformed. This is meant to be ran
    for each module/file in the process of transformation.
    """
    transformer = ImportModuleTransformer(tree, module_, wrappers)
    tree = transformer.visit(tree)

    return tree
