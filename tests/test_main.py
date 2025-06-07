import ast
import inspect

import array_api_strict

from array_api._2024_12 import ArrayNamespace, add


def test_main():
    assert isinstance(array_api_strict.add, add)
    # Namespace <= strict
    assert isinstance(array_api_strict, ArrayNamespace)
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
