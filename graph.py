from __future__ import annotations

import itertools as it
from functools import lru_cache

from symmetric_multi_dict import subdictionary, SymmetricMultiDict, _KT

from typing import Generic, Protocol, Sequence, TypeVar, Literal


ZERO_OR_ONE = Literal[0] | Literal[1]  # allowed values to take are either 0 or 1


_HC_VT = tuple[ZERO_OR_ONE, ...]  # hypercube graph vertex type


class ConnectivityMap(SymmetricMultiDict[_KT]):
    def __repr__(self) -> str:
        return f"ConnectivityMap({dict(self.items())})"


_VT = TypeVar("_VT")  # vertex type


def cycle_equal(p1: Sequence[_VT], p2: Sequence[_VT]) -> bool:
    s1, s2 = set(p1), set(p2)
    if len(s1) != len(s2):
        return False
    if s1.symmetric_difference(s2):
        return False
    # both are set equal

    # cycle stuff:
    l1, l2 = list(p1), list(p2)
    start = l1.index(l2[0])
    assert start >= 0  # alternatively, l2[0] in l1 is True

    l1 = l1[start:] + l1[:start]

    return all(e1 == e2 for e1, e2 in zip(l1, l2))


class Graph(Generic[_VT]):
    """Define methods that are common to all graphs here."""

    cmap: ConnectivityMap[_VT]
    paths: set[tuple[_VT, ...]]
    _dfs_paths: frozenset[tuple[_VT, ...]]
    _dfs_cycles: set[tuple[_VT, ...]]
    conn_comps: set[frozenset[_VT]]

    def __init__(self) -> None:
        """Returns empty graph"""
        self.cmap = ConnectivityMap()
        self.paths = set()
        self._dfs_paths = frozenset()  # to store temporary data during dfs
        self._dfs_cycles = set()  # to store temporary data during dfs
        self.conn_comps = set()

    @property
    def vertices(self) -> set[_VT]:
        return set(self.cmap.keys())

    def add_edge(self, v1: _VT, v2: _VT):
        self.cmap[v1] = v2
        assert v1 in self.cmap[v2]

    def _distance_in_path(self, v1: _VT, v2: _VT, path: tuple[_VT]) -> float:
        if v1 in path and v2 in path:
            return abs(path.index(v1) - path.index(v2))
        return float("inf")

    def distance(self, v1: _VT, v2: _VT) -> float:
        dist_list = [self._distance_in_path(v1, v2, path) for path in self._DFSUtil(v1)]
        return min(dist_list)

    @lru_cache
    def _DFSUtil(
        self, v: _VT, path: tuple[_VT, ...] | None = None
    ) -> frozenset[tuple[_VT, ...]]:
        if path is None:
            path = tuple()

        path += (v,)
        ret = set()
        # Recur for all the adj vertices
        n_branches = 0
        for neighbour in self.cmap[v]:
            if neighbour not in path:
                n_branches += 1
                ret.update(self._DFSUtil(neighbour, path))

        return frozenset({path} if n_branches == 0 else ret)

    def DFS(self):
        # designed to get connected components

        visited: set[_VT] = set()
        unvisited: set[_VT] = self.vertices.copy()

        while unvisited:
            v = unvisited.pop()
            self._dfs_paths = self._DFSUtil(v)

            conn_comp_elems = frozenset(_v for _p in self._dfs_paths for _v in _p)
            self.conn_comps.add(conn_comp_elems)
            self.paths.update(self._dfs_paths)
            visited.update(conn_comp_elems)
            unvisited.difference_update(visited)

        assert visited == self.vertices


# class Hypercube(Graph[_HC_VT]):
#     def __init__(self, n: int) -> None:
#         CHOICES = (0, 1)
#         self.vertices: list[_HC_VT] = list(it.product(CHOICES, repeat=n))
#         # gives the cartesian product {0, 1}^n as a list of tuples
#         # ie. [(0, 0, 0), (0, 0, 1), (0, 1, 0), (0, 1, 1), (1, 0, 0), (1, 0, 1), (1, 1, 0), (1, 1, 1)], for n=3
