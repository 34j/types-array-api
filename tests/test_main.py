import array_api_strict

from array_api._2024_12 import ArrayNamespace, add


def test_main():
    assert isinstance(array_api_strict.add, add)
    assert isinstance(array_api_strict, ArrayNamespace)
