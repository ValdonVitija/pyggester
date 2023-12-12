import ast
import astor
from pyggester.observable_transformations import (
    ObservableCollectorAppender,
    ObservableRunner,
    apply_observable_collector_transformations,
)


def test_observable_collector_appender():
    source_code = "list_ = ObservableList([1,2,3])"
    tree = ast.parse(source_code)
    transformer = ObservableCollectorAppender()
    transformed_tree = transformer.visit(tree)

    transformed_code = astor.to_source(transformed_tree)
    assert "OBSERVABLE_COLLECTOR.append(list_)" in transformed_code


def test_observable_runner():
    tree = ast.parse("import module1\nimport module2")
    transformer = ObservableRunner()
    transformed_tree = transformer.visit(tree)

    transformed_code = astor.to_source(transformed_tree)

    assert "for observable in OBSERVABLE_COLLECTOR:" in transformed_code
    assert "observable.run()" in transformed_code


def test_apply_observable_collector_transformations():
    source_code = "import module1\nimport module2"
    tree = ast.parse(source_code)
    transformed_code = apply_observable_collector_transformations(
        tree, run_observables=True
    )

    assert (
        "from pyggester.observables import" in transformed_code
        or "import pyggester.observables" in transformed_code
    )
