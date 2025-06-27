from __future__ import annotations

import ast
import warnings
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
        A ProtocolData object containing the converted function definition.

    """
    stmt = deepcopy(stmt)
    name = stmt.name
    docstring = ast.get_docstring(stmt, False)
    stmt.name = "__call__"
    stmt.body = [ast.Expr(value=ast.Constant(value=Ellipsis))]
    stmt.args.posonlyargs.insert(0, ast.arg(arg="self"))
    stmt.decorator_list.append(ast.Name(id="abstractmethod"))
    # Literal[inf] not allowed
    if "norm" in name:
        stmt.type_comment = "ignore[valid-type]"
    # __array_namespace_info__ is a special case
    if isinstance(stmt.returns, ast.Name) and stmt.returns.id == "Info":
        stmt.returns = ast.Subscript(
            value=ast.Name(id="Info"),
            slice=ast.Tuple(
                elts=[ast.Name(id=t.name) for t in typevars if t.name in ["device"]],
                ctx=ast.Load(),
            ),
        )
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
        body=([ast.Expr(value=ast.Constant(docstring))] if docstring is not None else []) + [stmt],
        type_params=[ast.TypeVar(name=t.name, bound=ast.Name(id=t.bound) if t.bound else None) for t in typevars],
    )
    return ProtocolData(
        stmt=stmt_new,
        typevars_used=typevars,
    )


def _class_to_protocol(stmt: ast.ClassDef, typevars: Sequence[TypeVarInfo]) -> ProtocolData:
    """
    Convert a class definition to a Protocol class.

    Parameters
    ----------
    stmt : ast.ClassDef
        The class definition to convert.
    typevars : Sequence[TypeVarInfo]
        The type variables used in the class.

    Returns
    -------
    ProtocolData
        The ProtocolData object containing the converted class definition.

    """
    unp = ast.unparse(stmt)
    # extract type variables from the class definition
    typevars = [typevar for typevar in typevars if f": {typevar.name}" in unp or f"-> {typevar.name}" in unp or f"[{typevar.name}]" in unp]
    # Array must not be a generic of itself
    if stmt.name == "_array":
        typevars = [t for t in typevars if t.name != "array"]
        for node in ast.walk(stmt):
            if isinstance(node, ast.Name) and node.id == "array":
                node.id = "Self"
        stmt.name = "_array"
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
            if b.name == "__array_namespace__":
                b.returns = ast.Subscript(
                    value=ast.Name(id="ArrayNamespace"),
                    slice=ast.Tuple(
                        elts=[ast.Name(x) for x in ("Self", "dtype", "device")],
                        ctx=ast.Load(),
                    ),
                )
    stmt.type_params = [ast.TypeVar(name=t.name, bound=ast.Name(id=t.bound) if t.bound else None) for t in typevars]
    stmt.decorator_list = [ast.Name(id="runtime_checkable")]
    return ProtocolData(
        stmt=stmt,
        typevars_used=typevars,
    )


def _attributes_to_protocol(name: str, attributes: Sequence[ModuleAttributes], /, *, typevars: Sequence[TypeVarInfo], bases: list[ast.expr] | None = None, typevars_force: Sequence[TypeVarInfo] | None = None) -> ProtocolData:
    """
    Convert a list of module attributes to a Protocol class.

    Parameters
    ----------
    name : str
        The name of the Protocol class.
    attributes : Sequence[ModuleAttributes]
        The attributes to include in the Protocol class.
    bases : list[ast.expr] | None, optional
        The base classes for the Protocol class, by default None, which defaults to [Protocol].
    typevars : Sequence[TypeVarInfo]
        The type variables used in the class.
    typevars_force : Sequence[TypeVarInfo] | None, optional
        The type variables used in the Protocol class, by default None, which defaults to the type variables used in the attributes.

    Returns
    -------
    ProtocolData
        The ProtocolData object containing the converted attributes.

    """
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
    if typevars_force is None:
        typevars_force = [t for t in typevars if any(t in attr.typevars_used for attr in attributes)]
    return ProtocolData(
        stmt=ast.ClassDef(
            name=name,
            decorator_list=[ast.Name(id="runtime_checkable")],
            keywords=[],
            bases=(bases if bases else [])
            + [
                ast.Name(id="Protocol"),
            ],
            body=body,
            type_params=[ast.TypeVar(name=t.name, bound=ast.Name(id=t.bound) if t.bound else None) for t in typevars_force],
        ),
        typevars_used=typevars_force,
    )


def generate(body_module: dict[str, list[ast.stmt]], out_path: Path) -> None:
    """
    Generate Protocol classes from the given module body.

    Parameters
    ----------
    body_module : dict[str, list[ast.stmt]]
        The module body containing the AST statements for each submodule.
    out_path : Path
        The output path where the generated Protocol classes will be saved.

    """
    body_module["_types"]
    del body_module["__init__"]

    # Get all TypeVars
    typevars = [TypeVarInfo("array", "_array"), TypeVarInfo("dtype"), TypeVarInfo("device"), TypeVarInfo("_T_co")]

    # Dict of module attributes per submodule
    module_attributes: defaultdict[str, list[ModuleAttributes]] = defaultdict(list)

    # Import `abc.abstractmethod`, `typing.Protocol` and `typing.runtime_checkable`
    out = ast.Module(body=[], type_ignores=[])

    # Create Protocols with __call__, representing functions
    for submodule, body in body_module.items():
        for i, b in enumerate(body):
            if isinstance(b, (ast.Import, ast.ImportFrom)):
                pass
            elif isinstance(b, ast.FunctionDef):
                # implemented in object rather than Namespace
                if b.name == "__eq__":
                    continue
                # info.py conntains functions which are not part of the Namespace (but Info class)
                if submodule == "info" and b.name != "__array_namespace_info__":
                    continue
                data = _function_to_protocol(b, typevars)
                docstring = ast.get_docstring(b)
                # add to module attributes
                module_attributes[submodule].append(ModuleAttributes(b.name, data.name, docstring, data.typevars_used))
                # some functions are duplicated in linalg and fft, skip them
                # their docstrings are unhelpful, e.g. "Alias for ..."
                if "Alias" in (ast.get_docstring(b) or ""):
                    continue
                # add to output
                out.body.append(data.stmt)
            elif isinstance(b, ast.Assign):
                # _types.py contains Assigns which are not part of the Namespace
                if submodule == "_types":
                    if isinstance(b.targets[0], ast.Name) and b.targets[0].id in ["Capabilities", "DefaultDataTypes", "DataTypes"]:
                        b = ast.parse(ast.unparse(b).replace("dtype", "Any"))  # type: ignore
                        out.body = [b, *out.body]
                    continue
                if not isinstance(b.targets[0], ast.Name):
                    continue
                id = b.targets[0].id
                # __init__.py
                if id == "__all__":
                    continue
                # weird assignment
                if id == "array":
                    continue
                # get docstring
                docstring = None
                if i != len(body) - 1:
                    docstring_expr = body[i + 1]
                    if isinstance(docstring_expr, ast.Expr):
                        if isinstance(docstring_expr.value, ast.Constant):
                            docstring = docstring_expr.value.value
                # add to module attributes
                module_attributes[submodule].append(ModuleAttributes(id, ast.Name(id="array"), docstring, []))
            elif isinstance(b, ast.ClassDef):
                data = _class_to_protocol(b, typevars)
                # add to output, do not add to module attributes
                # add to first position
                out.body.insert(0, data.stmt)
            elif isinstance(b, ast.Expr):
                pass
            else:
                warnings.warn(f"Skipping {submodule} {b}", stacklevel=2)

    # Manual addition
    for d in ["bool", "complex128", "complex64", "float32", "float64", "int16", "int32", "int64", "int8", "uint16", "uint32", "uint64", "uint8"]:
        module_attributes[""].append(ModuleAttributes(d, ast.Name("dtype"), None, []))
    module_attributes[""].append(ModuleAttributes("Device", ast.Name("device"), None, []))

    # Create Protocols for the main namespace
    OPTIONAL_SUBMODULES = ["fft", "linalg"]
    main_attributes = [attribute for submodule, attributes in module_attributes.items() for attribute in attributes if submodule not in OPTIONAL_SUBMODULES]
    main_protocol = _attributes_to_protocol("ArrayNamespace", main_attributes, typevars=typevars).stmt
    out.body.append(main_protocol)

    # Create Protocols for fft and linalg
    submodules: list[ModuleAttributes] = []
    for submodule, attributes in module_attributes.items():
        if submodule not in OPTIONAL_SUBMODULES:
            continue
        data = _attributes_to_protocol(submodule[0].upper() + submodule[1:] + "Namespace", attributes, typevars=typevars)
        out.body.append(data.stmt)
        if submodule in OPTIONAL_SUBMODULES:
            submodules.append(ModuleAttributes(submodule, data.name, None, [t for t in typevars if any(t in attr.typevars_used for attr in attributes)]))

    # Create Full Protocol for the main namespace
    out.body.append(_attributes_to_protocol("ArrayNamespaceFull", submodules, bases=[ast.Subscript(ast.Name("ArrayNamespace"), ast.Tuple([ast.Name(t.name) for t in main_protocol.type_params]))], typevars=typevars, typevars_force=[t for t in typevars if t.name in [s.name for s in main_protocol.type_params]]).stmt)  # type: ignore

    # Replace TypeVars because of the name conflicts like "array: array"
    for node in ast.walk(out):
        for child in ast.iter_child_nodes(node):
            if isinstance(child, ast.Name) and child.id in {t.name for t in typevars}:
                if isinstance(node, ast.AnnAssign):
                    node.annotation = ast.Name(id="T" + child.id.capitalize())
                else:
                    child.id = "T" + child.id.capitalize()
            elif isinstance(child, ast.TypeVar) and child.name in {t.name for t in typevars}:
                child.name = "T" + child.name.capitalize()

    # Replace _array with Array
    for node in ast.walk(out):
        if isinstance(node, ast.Name) and node.id == "_array":
            node.id = "Array"
        if isinstance(node, ast.ClassDef) and node.name == "_array":
            node.name = "Array"

    # Manual modifications (easier than AST manipulations)
    text = ast.unparse(ast.fix_missing_locations(out))

    # Add imports
    text = (
        """from __future__ import annotations

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
    TypedDict,
)
from types import EllipsisType as ellipsis
from typing_extensions import CapsuleType as PyCapsule
from typing_extensions import Self
from collections.abc import Buffer as SupportsBufferProtocol
inf = float("inf")

"""
        + text
        + """
@runtime_checkable
class ShapedArray[*T, TDevice, TDtype](Array[TDevice, TDtype], Protocol):
    @property
    def shape(self) -> tuple[*T]: ...  # type: ignore[override]


type ShapedAnyArray[*T] = ShapedArray[*T, Any, Any]
"""
    )

    # Fix self-references in typing
    ns = "Union[T_t_co, NestedSequence[T_t_co]]"
    text = text.replace(ns, f'"{ns}"')

    # write to the output path
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(text, "utf-8")


def generate_all(
    cache_dir: Path | str = ".cache",
    out_path: Path | str = "src/array_api",
) -> None:
    """
    Clone the array-api repository and generate Protocol classes for all versions.

    Parameters
    ----------
    cache_dir : Path | str, optional
        The directory where the array-api repository will be cloned, by default ".cache"
    out_path : Path | str, optional
        The output path where the generated Protocol classes will be saved, by default "src/array_api"

    """
    import subprocess as sp

    Path(cache_dir).mkdir(exist_ok=True)
    sp.run(["git", "clone", "https://github.com/data-apis/array-api", ".cache"])

    for dir_path in (Path(cache_dir) / Path("src") / "array_api_stubs").iterdir():
        # skip non-directory entries
        if not dir_path.is_dir():
            continue
        # 2021 is broken (no self keyword in `_array`` methods)
        if "2021" in dir_path.name:
            continue
        # get module bodies
        body_module = {path.stem: ast.parse(path.read_text("utf-8").replace("self: array", "self").replace("Dtype", "dtype").replace("Device", "device")).body for path in dir_path.rglob("*.py")}
        generate(body_module, (Path(out_path) / dir_path.name).with_suffix(".py"))
