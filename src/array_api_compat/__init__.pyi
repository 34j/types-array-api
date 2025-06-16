from typing import Any, Literal

from array_api._2024_12 import Array, ArrayNamespaceFull

# return full namespace for convenience
# because optional attributes are not supported
def array_namespace[TArray: Array](
    *xs: TArray | complex | None,
    api_version: Literal["2024.12"] | None = None,
    use_compat: bool | None = None,
) -> ArrayNamespaceFull[TArray, Any, Any, Any, Any, Any]: ...
