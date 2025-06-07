from __future__ import annotations

import ast
from collections import defaultdict
from collections.abc import Mapping, Sequence
from copy import deepcopy
from pathlib import Path

import attrs


@attrs.frozen()
class ProtocolData:
    stmt: ast.ClassDef
    typevars_used: Sequence[str]
    name: str




def _function_to_protocol(stmt: ast.FunctionDef, typevars: list[str]) -> ProtocolData:
    """
    Convert a function definition to a Protocol class.

    Parameters
    ----------
    stmt : ast.FunctionDef
        The function definition to convert.
    typevars : list[str]
        The list of TypeVars to include in the Protocol.

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
    args = ast.unparse(stmt.args)
    typevars = [typevar for typevar in typevars if typevar in args]

    # Construct the protocol
    stmt_new = ast.ClassDef(
        name=name,
        decorator_list=[ast.Name(id="runtime_checkable")],
        keywords=[],
        bases=[
            ast.Subscript(
                value=ast.Name(id="Protocol"),
                slice=ast.Tuple(elts=[ast.Name(typevar) for typevar in typevars]),
            )
        ],
        body=([ast.Expr(value=ast.Constant(docstring, kind=None))] if docstring is not None else []) + [stmt],
        type_params=[],
    )  # type: ignore[call-arg]
    return ProtocolData(
        stmt=stmt_new,
        typevars_used=typevars,
        name=name + (f"[{', '.join(typevars)}]" if typevars else ""),
    )

def _class_to_protocol(
    stmt: ast.ClassDef, typevars: list[str]
) -> ProtocolData:
    typevars = [typevar for typevar in typevars if typevar in ast.unparse(stmt)]
    stmt.bases = [
        ast.Subscript(
            value=ast.Name(id="Protocol"),
            slice=ast.Tuple(elts=[ast.Name(typevar) for typevar in typevars]),
        )
    ]
    return ProtocolData(
        stmt=stmt,
        typevars_used=typevars,
        name=stmt.name + (f"[{', '.join(typevars)}]" if typevars else ""),
    )

def _attributes_to_protocol(
    name, attributes: list[tuple[str, str, str | None, list]], typevars: list[str]
) -> ProtocolData:
    body = []
    for attribute, type, docstring, _ in attributes:
        body.append(
            ast.AnnAssign(
                target=ast.Name(id=attribute),
                annotation=ast.Name(id=type) if type is not None else None,
                simple=1,
            )
        )
        if docstring is not None:
            body.append(ast.Expr(value=ast.Constant(docstring)))

    typevars = {x for attribute in attributes for x in attribute[3]}
    return ProtocolData(
        stmt=ast.ClassDef(
            name=name,
            decorator_list=[ast.Name(id="runtime_checkable")],
            keywords=[],
            bases=[
                ast.Subscript(
                    value=ast.Name(id="Protocol"),
                    slice=ast.Tuple(elts=[ast.Name(typevar) for typevar in typevars]),
                )
            ],
            body=body,
            type_params=[],
        ),
        typevars_used=typevars,
        name=name + (f"[{', '.join(typevars)}]" if typevars else ""),
    )


def generate_all(
    cache_dir: Path | str = ".cache",
    out_path="src/array-api",
    out_name: str = "_namespace.py",
) -> None:
    import subprocess as sp

    Path(cache_dir).mkdir(exist_ok=True)
    sp.run(["git", "clone", "https://github.com/data-apis/array-api", ".cache"])

    for dir_path in (Path(cache_dir) / Path("src") / "array_api_stubs").glob("**/"):
        # get module bodies
        body_module = {
            path.stem: ast.parse(path.read_text("utf-8")).body
            for path in dir_path.rglob("*.py")
        }
        generate(body_module, Path(out_path) / dir_path.name / out_name)


def generate(body_module: Mapping[str, list[ast.stmt]], out_path: Path) -> None:
    body_typevars = body_module.get("_types")
    body_module.pop("__init__")

    # Get all TypeVars
    typevars = []
    for b in body_typevars:
        if isinstance(b, ast.Assign):
            value = b.value
            if isinstance(value, ast.Call):
                if value.func.id == "TypeVar":
                    typevars.append(value.args[0].s)
    print(typevars)

    # Dict of module attributes per submodule
    module_attributes = defaultdict(list)

    # Import `abc.abstractmethod`, `typing.Protocol` and `typing.runtime_checkable`
    out = ast.Module(body=[], type_ignores=[])
    out.body.append(
        ast.Expr(value=ast.Constant("Auto generated Protocol classes (Do not edit)"))
    )
    out.body.append(
        ast.ImportFrom(
            module="typing",
            names=[
                # ast.alias(name="Protocol", alias=None),
                # ast.alias(name="runtime_checkable", alias=None),
                ast.alias(name="*")
            ],
            level=0,
        ),
    )
    out.body.append(
        ast.ImportFrom(
            module="abc",
            names=[ast.alias(name="abstractmethod", alias=None)],
            level=0,
        ),
    )

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
                module_attributes[submodule].append(
                    (b.name, data.name, None, data.typevars_used)
                )
                out.body.append(data.stmt)
            elif isinstance(b, ast.Assign):
                if submodule == "_types":
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
                    module_attributes[submodule].append((id, "float", docstring, []))
            elif isinstance(b, ast.ClassDef):
                data = _class_to_protocol(b, typevars)
                out.body.append(data.stmt)
                module_attributes[submodule].append(
                    (b.name, data.name, None, data.typevars_used)
                )
            elif isinstance(b, ast.Expr):
                pass
            else:
                print(f"Skipping {submodule} {b} \n\n")

    # Create Protocols for fft and linalg
    submodules = []
    OPTIONAL_SUBMODULES = ["fft", "linalg"]
    for submodule, attributes in module_attributes.items():
        if submodule not in OPTIONAL_SUBMODULES:
            continue
        data = _attributes_to_protocol(
            submodule[0].upper() + submodule[1:] + "Namespace", attributes, typevars
        )
        out.body.append(data.stmt)
        if submodule in OPTIONAL_SUBMODULES:
            submodules.append((submodule, data.name, None, []))

    # Create Protocols for the main namespace
    attributes = [
        attribute
        for submodule, attributes in module_attributes.items()
        for attribute in attributes
        if submodule not in OPTIONAL_SUBMODULES
    ] + submodules
    out.body.append(
        _attributes_to_protocol("ArrayNamespace", attributes, typevars).stmt
    )
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(ast.unparse(out), "utf-8")
