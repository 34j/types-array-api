# Python array API standard typing

<p align="center">
  <a href="https://github.com/34j/types-array-api/actions/workflows/ci.yml?query=branch%3Amain">
    <img src="https://img.shields.io/github/actions/workflow/status/34j/array-api/ci.yml?branch=main&label=CI&logo=github&style=flat-square" alt="CI Status" >
  </a>
  <a href="https://array-api.readthedocs.io">
    <img src="https://img.shields.io/readthedocs/array-api.svg?logo=read-the-docs&logoColor=fff&style=flat-square" alt="Documentation Status">
  </a>
  <a href="https://codecov.io/gh/34j/array-api">
    <img src="https://img.shields.io/codecov/c/github/34j/array-api.svg?logo=codecov&logoColor=fff&style=flat-square" alt="Test coverage percentage">
  </a>
</p>
<p align="center">
  <a href="https://github.com/astral-sh/uv">
    <img src="https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/astral-sh/uv/main/assets/badge/v0.json" alt="uv">
  </a>
  <a href="https://github.com/astral-sh/ruff">
    <img src="https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/astral-sh/ruff/main/assets/badge/v2.json" alt="Ruff">
  </a>
  <a href="https://github.com/pre-commit/pre-commit">
    <img src="https://img.shields.io/badge/pre--commit-enabled-brightgreen?logo=pre-commit&logoColor=white&style=flat-square" alt="pre-commit">
  </a>
</p>
<p align="center">
  <a href="https://pypi.org/project/array-api/">
    <img src="https://img.shields.io/pypi/v/array-api.svg?logo=python&logoColor=fff&style=flat-square" alt="PyPI Version">
  </a>
  <img src="https://img.shields.io/pypi/pyversions/array-api.svg?style=flat-square&logo=python&amp;logoColor=fff" alt="Supported Python versions">
  <img src="https://img.shields.io/pypi/l/array-api.svg?style=flat-square" alt="License">
</p>

---

**Documentation**: <a href="https://array-api.readthedocs.io" target="_blank">https://array-api.readthedocs.io </a>

**Source Code**: <a href="https://github.com/34j/types-array-api" target="_blank">https://github.com/34j/types-array-api </a>

---

Typing for array API and array-api-compat

## Installation

Install this via pip (or your favourite package manager):

```shell
pip install types-array-api
```

## Usage

### Type stubs

Provices type stubs for [`array-api-compat`](https://data-apis.org/array-api-compat/).

```python
import array_api_compat

xp = array_api_compat.array_namespace(x)
```

![Screenshot 1](https://raw.githubusercontent.com/34j/array-api/main/docs/_static/screenshot1.png)
![Screenshot 2](https://raw.githubusercontent.com/34j/array-api/main/docs/_static/screenshot2.png)

### Array Type

```python
from array_api._2024_12 import Array


def my_function[TArray: Array](x: TArray) -> TArray:
    return x + 1
```

### Namespace Type

You can test if an object matches the Protocol by:

```python
import array_api_strict

from array_api._2024_12 import ArrayNamespace, ArrayNamespaceFull


assert isinstance(array_api_strict, ArrayNamespace)
# Full version contains fft and linalg
# fft and linalg are not included by default in array_api_strict
assert not isinstance(array_api_strict, ArrayNamespaceFull)
```

## Notes on the design concepts

### Regarding not supporting shape typing

#### Typing only ndim

Typing only the number of dimensions (ndim), as Numpy currently does, can be accomplished like `Array[tuple[int, int, int]]` or `Array[int, int, int]`.

However

- This approach requires many number of characters
- Requires (`2 * max_ndim` type overloads for each function) or (`2` type overloads for each function and `max_ndim` Protocol, and moreover user has to use these Protocols everywhere in their code) due to
- Tt does not indicate the meaning of each dimension (e.g., batch axis, vector axis, matrix axis, etc.).

## Contributors ✨

Thanks goes to these wonderful people ([emoji key](https://allcontributors.org/docs/en/emoji-key)):

<!-- prettier-ignore-start -->
<!-- ALL-CONTRIBUTORS-LIST:START - Do not remove or modify this section -->
<!-- markdownlint-disable -->
<!-- markdownlint-enable -->
<!-- ALL-CONTRIBUTORS-LIST:END -->
<!-- prettier-ignore-end -->

This project follows the [all-contributors](https://github.com/all-contributors/all-contributors) specification. Contributions of any kind welcome!

## Credits

[![Copier](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/copier-org/copier/master/img/badge/badge-grayscale-inverted-border-orange.json)](https://github.com/copier-org/copier)

This package was created with
[Copier](https://copier.readthedocs.io/) and the
[browniebroke/pypackage-template](https://github.com/browniebroke/pypackage-template)
project template.
