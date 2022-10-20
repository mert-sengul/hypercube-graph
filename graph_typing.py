from __future__ import annotations
from collections import defaultdict


from typing import Any, Callable, Literal, FrozenSet, TypeVar

_KT = TypeVar("_KT")

ZERO_OR_ONE = Literal[0] | Literal[1]  # allowed values to take are either 0 or 1

VERTEX_T = tuple[ZERO_OR_ONE, ...]


class MultiDict(defaultdict[_KT, set[_KT]]):
    default_factory: Callable[[], set]

    def __init__(self, *args, **kwargs):
        if len(args):
            args = args[1:]
        super(MultiDict, self).__init__(set, *args, **kwargs)
        assert self.default_factory

    def __setitem__(self, __key: _KT, __value: _KT, **kwargs) -> None:
        if __key not in self:
            self.__missing__(__key)
        super().__getitem__(__key).add(__value)

    def __missing__(self, __key: _KT):
        # called by __getitem__ and __setitem__ when the item is missing
        value = self.default_factory()
        super().__setitem__(__key, value)
        return value


class SymmetricMultiDict(MultiDict[_KT]):
    def __setitem__(self, __key: _KT, __value: _KT) -> None:
        if __key == __value:
            raise ValueError(f"key==value=={__key}")

        super().__setitem__(__value, __key)
        return super().__setitem__(__key, __value)


class ConnectivityMap(SymmetricMultiDict[VERTEX_T]):
    ...


if __name__ == "__main__":
    m = ConnectivityMap()
    v = (0, 0)
    u = (0, 1)
    m[v]
    m[v]
    m[v] = u
    assert m[v] == {u}
    assert m[u] == {v}
    print()
