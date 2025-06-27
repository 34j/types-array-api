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

Autocompletion for [`array-api-compat`](https://data-apis.org/array-api-compat/) is available in your IDE **just by installing** this package.

```python
import array_api_compat

xp = array_api_compat.array_namespace(x)
```

![Screenshot 1](https://raw.githubusercontent.com/34j/array-api/main/docs/_static/screenshot1.png)
![Screenshot 2](https://raw.githubusercontent.com/34j/array-api/main/docs/_static/screenshot2.png)

### Typineg your function using `Array`

There are multiple ways to type your functions:

- This is the simplest way to enjoy autocompletion for `Array`. Practically this should be enough for most use cases.

  ```python
  from array_api._2024_12 import Array, ShapedAnyArray

  def simple(x: Array) -> Array:
      return x + 1
  ```

- If you want to make sure that the same type of array (`ndarray`→`ndarray`, `Tensor`→`Tensor`) is returned, you can use `Array` with a type variable.

  ```python
  def generic[TArray: Array](x: TArray) -> TArray:
      return x + 1
  ```

## Advanced Usage

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

### Shape Typing

- If you want to make sure about the input and output shapes, you can use `ShapedArray`:

  ```python
  from array_api._2024_12 import ShapedAnyArray as Array

  def sum_last_axis[*TShape](x: Array[*TShape, Any]) -> Array[*TShape]:
      return xp.sum(x, axis=-1)
  ```

  More complex example using [NewType](https://docs.python.org/3/library/typing.html#newtype) or [type aliases](https://docs.python.org/3/library/typing.html#type-aliases):

  ```python
  RTheta = NewType("RTheta", int)
  XY = NewType("XY", int)
  def polar_coordinates[*TShape](randtheta: Array[*TShape, RTheta]) -> Array[*TShape, XY]:
      """Convert polar coordinates to Cartesian coordinates."""
      r = randtheta[..., 0]
      theta = randtheta[..., 1]
      x = r * xp.cos(theta)
      y = r * xp.sin(theta)
      return xp.stack((x, y), axis=-1)
  ```

  Note that `ShapedAnyArray` exists only for **documentation purposes** and internally it is treated as `Array`.
  Using both generic and shaped are impossible due to [python/typing#548](https://github.com/python/typing/issues/548).

- Note that the below example is ideal but impossible due to Python specification.

  ```python
  def impossible[
      TDtype,
      TDevice,
      *TShapeFormer: int,
      *TShapeLatter: int,
      TArray: Array
  ](x: TArray[*TShapeFormer, *TShapeLatter | Literal[1], TDtype, TDevice], y: TArray[*TShapeLatter | Literal[1], TDtype, TDevice]) -> TArray[*TShapeFormer, *TShapeLatter, TDtype, TDevice]:
      return x + y # broadcasting
  ```

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
