from typing import Any, Literal

from array_api._2024_12 import Array, ArrayNamespace

def array_namespace[TArray: Array](
    *xs: TArray | complex | None,
    api_version: Literal["2024.12"] | None = None,
    use_compat: bool | None = None,
) -> ArrayNamespace[TArray, Any, Any, Any, Any, Any]: ...
