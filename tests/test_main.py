import ast
import inspect

import array_api_strict

from array_api.latest import ArrayNamespace


def test_strict_supset_namespace():
    # Namespace <= strict
    assert isinstance(array_api_strict, ArrayNamespace)
    # module = ast.parse(inspect.getsource(ArrayNamespace))
    # classdef = next(n for n in module.body if isinstance(n, ast.ClassDef) and n.name == "ArrayNamespace")
    # for n in classdef.body:
    #     if not isinstance(n, ast.AnnAssign):
    #         continue
    #     if not isinstance(n.target, ast.Name):
    #         continue
    #     if not isinstance(n.annotation, ast.Subscript):
    #         continue
    #     if not isinstance(n.annotation.value, ast.Name):
    #         continue
    #     assert isinstance(
    #         getattr(array_api_strict, n.target.id, None),
    #         getattr(array_api._2024_12, n.annotation.value.id, None)
    #     )


def test_namespace_supset_strict():
    # Namespace >= strict
    missing = []
    module = ast.parse(inspect.getsource(ArrayNamespace))
    classdef = next(n for n in module.body if isinstance(n, ast.ClassDef) and n.name == "ArrayNamespace")
    names = [n.target.id for n in classdef.body if isinstance(n, ast.AnnAssign) and isinstance(n.target, ast.Name)]
    for attr in dir(array_api_strict):
        if attr.startswith("_"):
            continue
        if "trict" in attr:
            continue
        if attr not in names:
            missing.append(attr)
    assert not missing, f"Missing attributes in ArrayNamespace: {missing}"
