from __future__ import annotations

import ast
import runpy
from collections import defaultdict
from collections.abc import Iterable, Sequence
from copy import deepcopy
from pathlib import Path

import attrs


@attrs.frozen()
class TypeVarInfo:
    name: str
    bound: str | None = None


@attrs.frozen()
class ProtocolData:
    stmt: ast.ClassDef
    typevars_used: Iterable[TypeVarInfo]

    @property
    def name(self) -> ast.Subscript:
        return ast.Subscript(
            value=ast.Name(id=self.stmt.name, ctx=ast.Load()),
            slice=ast.Tuple(
                elts=[ast.Name(id=t.name) for t in self.typevars_used],
                ctx=ast.Load(),
            ),
            ctx=ast.Load(),
        )


@attrs.frozen()
class ModuleAttributes:
    name: str
    type: ast.expr
    docstring: str | None
    typevars_used: Iterable[TypeVarInfo]


def _function_to_protocol(stmt: ast.FunctionDef, typevars: Sequence[TypeVarInfo]) -> ProtocolData:
    """
    Convert a function definition to a Protocol class.

    Parameters
    ----------
    stmt : ast.FunctionDef
        The function definition to convert.
    typevars : Sequence[TypeVarInfo]
        The type variables used in the function.

    Returns
    -------
    ProtocolData
        A ProtocolData object.

    """
    stmt = deepcopy(stmt)
    name = stmt.name
    docstring = ast.get_docstring(stmt)
    stmt.name = "__call__"
    stmt.body = [ast.Expr(value=ast.Constant(value=Ellipsis))]
    stmt.args.posonlyargs.insert(0, ast.arg(arg="self"))
    stmt.decorator_list.append(ast.Name(id="abstractmethod"))
    if "norm" in name:
        stmt.type_comment = "ignore[valid-type]"
    args = ast.unparse(stmt.args) + (ast.unparse(stmt.returns) if stmt.returns else "")
    typevars = [typevar for typevar in typevars if typevar.name in args]

    # Construct the protocol
    stmt_new = ast.ClassDef(
        name=name,
        decorator_list=[ast.Name(id="runtime_checkable")],
        keywords=[],
        bases=[
            ast.Name(id="Protocol"),
        ],
        body=([ast.Expr(value=ast.Constant(docstring, kind=None))] if docstring is not None else []) + [stmt],
        type_params=[ast.TypeVar(name=t.name, bound=ast.Name(id=t.bound) if t.bound else None) for t in typevars],
    )
    return ProtocolData(
        stmt=stmt_new,
        typevars_used=typevars,
    )


def _class_to_protocol(stmt: ast.ClassDef, typevars: Sequence[TypeVarInfo]) -> ProtocolData:
    unp = ast.unparse(stmt)
    typevars = [typevar for typevar in typevars if typevar.name in unp]
    stmt.bases = [
        ast.Name(id="Protocol"),
    ]
    for b in stmt.body:
        if isinstance(b, ast.FunctionDef):
            if getattr(b.body[-1].value, "value", None) is Ellipsis:  # type: ignore[attr-defined]
                pass
            else:
                b.body.append(ast.Expr(value=ast.Constant(value=Ellipsis)))
            if b.name in ["__eq__", "__ne__"]:
                b.type_comment = "ignore[override]"
    stmt.type_params = [ast.TypeVar(name=t.name, bound=ast.Name(id=t.bound) if t.bound else None) for t in typevars]
    stmt.decorator_list = [ast.Name(id="runtime_checkable")]
    return ProtocolData(
        stmt=stmt,
        typevars_used=typevars,
    )


def _attributes_to_protocol(name: str, attributes: Sequence[ModuleAttributes]) -> ProtocolData:
    body: list[ast.stmt] = []
    for a in attributes:
        body.append(
            ast.AnnAssign(
                target=ast.Name(id=a.name),
                annotation=a.type,
                simple=1,
            )
        )
        if a.docstring is not None:
            body.append(ast.Expr(value=ast.Constant(a.docstring)))

    typevars = sorted({x for attribute in attributes for x in attribute.typevars_used}, key=lambda x: x.name)
    return ProtocolData(
        stmt=ast.ClassDef(
            name=name,
            decorator_list=[ast.Name(id="runtime_checkable")],
            keywords=[],
            bases=[
                ast.Name(id="Protocol"),
            ],
            body=body,
            type_params=[ast.TypeVar(name=t.name, bound=ast.Name(id=t.bound) if t.bound else None) for t in typevars],
        ),
        typevars_used=typevars,
    )


def generate(body_module: dict[str, list[ast.stmt]], out_path: Path) -> None:
    body_typevars = body_module["_types"]
    del body_module["__init__"]

    # Get all TypeVars
    typevars: list[TypeVarInfo] = []
    for b in body_typevars:
        if isinstance(b, ast.Assign):
            value = b.value
            if isinstance(value, ast.Call):
                if isinstance(value.func, ast.Name):
                    if value.func.id == "TypeVar":
                        if isinstance(value.args[0], ast.Constant):
                            name = value.args[0].s
                            typevars.append(
                                TypeVarInfo(
                                    name=name,
                                    bound={
                                        "array": "_array",
                                    }.get(name, None),
                                )
                            )
    typevars += [TypeVarInfo(name=x) for x in ["Capabilities", "DefaultDataTypes", "DataTypes"]]
    typevars = sorted(typevars, key=lambda x: x.name)

    # Dict of module attributes per submodule
    module_attributes: defaultdict[str, list[ModuleAttributes]] = defaultdict(list)

    # Import `abc.abstractmethod`, `typing.Protocol` and `typing.runtime_checkable`
    out = ast.Module(body=[], type_ignores=[])

    # Create Protocols with __call__, representing functions
    for submodule, body in body_module.items():
        for i, b in enumerate(body):
            if isinstance(b, (ast.Import, ast.ImportFrom)):
                pass
                # out.body.insert(0, b)
            elif isinstance(b, ast.FunctionDef):
                if b.name.startswith("_"):
                    continue
                data = _function_to_protocol(b, typevars)
                module_attributes[submodule].append(ModuleAttributes(b.name, data.name, None, data.typevars_used))
                if "Alias" in (ast.get_docstring(b) or ""):
                    continue
                out.body.append(data.stmt)
            elif isinstance(b, ast.Assign):
                if submodule == "_types":
                    continue
                if not isinstance(b.targets[0], ast.Name):
                    continue
                id = b.targets[0].id
                if id == "__all__":
                    pass
                else:
                    docstring = None
                    if i != len(body) - 1:
                        docstring_expr = body[i + 1]
                        if isinstance(docstring_expr, ast.Expr):
                            if isinstance(docstring_expr.value, ast.Constant):
                                docstring = docstring_expr.value.value
                    module_attributes[submodule].append(ModuleAttributes(id, ast.Name(id="float"), docstring, []))
            elif isinstance(b, ast.ClassDef):
                data = _class_to_protocol(b, typevars)
                out.body.append(data.stmt)
                # module_attributes[submodule].append(
                #     ModuleAttributes(b.name, data.name, None, data.typevars_used)
                # )
            elif isinstance(b, ast.Expr):
                pass
            else:
                print(f"Skipping {submodule} {b} \n\n")

    # Create Protocols for fft and linalg
    submodules: list[ModuleAttributes] = []
    OPTIONAL_SUBMODULES = ["fft", "linalg"]
    for submodule, attributes in module_attributes.items():
        if submodule not in OPTIONAL_SUBMODULES:
            continue
        data = _attributes_to_protocol(submodule[0].upper() + submodule[1:] + "Namespace", attributes)
        out.body.append(data.stmt)
        if submodule in OPTIONAL_SUBMODULES:
            submodules.append(ModuleAttributes(submodule, data.name, None, []))

    # Create Protocols for the main namespace
    attributes = [attribute for submodule, attributes in module_attributes.items() for attribute in attributes if submodule not in OPTIONAL_SUBMODULES] + submodules
    out.body.append(_attributes_to_protocol("ArrayNamespace", attributes).stmt)

    for node in ast.walk(out):
        for child in ast.iter_child_nodes(node):
            if isinstance(child, ast.Name) and child.id in {t.name for t in typevars}:
                if isinstance(node, ast.AnnAssign):
                    node.annotation = ast.Name(id="T" + child.id.capitalize())
                else:
                    child.id = "T" + child.id.capitalize()
            elif isinstance(child, ast.TypeVar) and child.name in {t.name for t in typevars}:
                child.name = "T" + child.name.capitalize()

    text = ast.unparse(ast.fix_missing_locations(out))
    text = (
        """"Auto generated Protocol classes (Do not edit)"
from enum import Enum
from abc import abstractmethod
from collections.abc import Sequence
from typing import (
    Any,
    Literal,
    Optional,
    Protocol,
    Union,
    Tuple,
    List,
    runtime_checkable,
)
inf = float("inf")
"""
        + text
    )
    ns = "Union[T_t_co, NestedSequence[T_t_co]]"
    text = text.replace(ns, f'"{ns}"')
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(text, "utf-8")


def generate_all(
    cache_dir: Path | str = ".cache",
    out_path: Path | str = "src/array_api",
) -> None:
    import subprocess as sp

    Path(cache_dir).mkdir(exist_ok=True)
    sp.run(["git", "clone", "https://github.com/data-apis/array-api", ".cache"])

    for dir_path in (Path(cache_dir) / Path("src") / "array_api_stubs").iterdir():
        if not dir_path.is_dir():
            continue
        if "2021" in dir_path.name:
            continue
        # get module bodies
        body_module = {path.stem: ast.parse(path.read_text("utf-8").replace("Dtype", "dtype").replace("Device", "device")).body for path in dir_path.rglob("*.py")}
        generate(body_module, (Path(out_path) / dir_path.name).with_suffix(".py"))

    import sys

    sys.argv = ["ssort", "src/array_api"]
    runpy.run_module("ssort")
    runpy.run_module("ruff")
