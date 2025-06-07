from typing import Any, Literal

from array_api._2024_12 import ArrayNamespace


def array_namespace(
    *xs: Any | complex | None,
    api_version: Literal["v2024.12"] | None = None,
    use_compat: bool | None = None,
) -> ArrayNamespace: ...
