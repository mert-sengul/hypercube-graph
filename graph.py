from __future__ import annotations

import itertools as it

from symmetric_multi_dict import subdictionary, SymmetricMultiDict, _KT

from typing import Generic, TypeVar, Literal


ZERO_OR_ONE = Literal[0] | Literal[1]  # allowed values to take are either 0 or 1

_VT = TypeVar("_VT")  # vertex type

_HC_VT = tuple[ZERO_OR_ONE, ...]  # hypercube graph vertex type


class ConnectivityMap(SymmetricMultiDict[_KT]):
    def __repr__(self) -> str:
        return f"ConnectivityMap({dict(self.items())})"


class Graph(Generic[_VT]):
    """Define methods that are common to all graphs here."""

    cmap: ConnectivityMap[_VT]
    paths: set[tuple[_VT]]
    _dfs_paths: set[tuple[_VT]]
    conn_comps: set[frozenset[_VT]]

    def __init__(self) -> None:
        """Returns empty graph"""
        self.cmap = ConnectivityMap()
        self.paths = set()
        self._dfs_paths = set()  # to store temporary data during dfs
        self._dfs_cycles = set()  # to store temporary data during dfs
        self.conn_comps = set()

    @property
    def vertices(self) -> set[_VT]:
        return set(self.cmap.keys())

    def add_edge(self, v1: _VT, v2: _VT):
        self.cmap[v1] = v2
        assert v1 in self.cmap[v2]

    def distance(self, v1: _VT, v2: _VT) -> int:
        ...

    def _DFSUtil(self, v: _VT, path: list[_VT] | None = None):
        if path is None:
            path = []

        path.append(v)

        # Recur for all the adj vertices
        n_branches = 0
        for neighbour in self.cmap[v]:
            if neighbour not in path:
                n_branches += 1
                self._DFSUtil(neighbour, path.copy())

        if n_branches == 0:
            # end of the path. path must be hashable.
            self._dfs_paths.add(tuple(path))

        if path[0] in self.cmap[v]:
            # a cycle
            self._dfs_cycles.add(tuple(path))

    def DFS(self):
        visited: set[_VT] = set()
        unvisited: set[_VT] = self.vertices.copy()

        while unvisited:
            self._dfs_paths.clear()
            v = unvisited.pop()
            self._DFSUtil(v)
            conn_comp_elems = frozenset(_v for _p in self._dfs_paths for _v in _p)
            self.conn_comps.add(conn_comp_elems)
            self.paths.update(self._dfs_paths)
            visited.update(conn_comp_elems)
            unvisited.difference_update(visited)

        assert visited == self.vertices


class Hypercube(Graph[_HC_VT]):
    def __init__(self, n: int) -> None:
        CHOICES = (0, 1)
        self.vertices: list[_HC_VT] = list(it.product(CHOICES, repeat=n))
        # gives the cartesian product {0, 1}^n as a list of tuples
        # ie. [(0, 0, 0), (0, 0, 1), (0, 1, 0), (0, 1, 1), (1, 0, 0), (1, 0, 1), (1, 1, 0), (1, 1, 1)], for n=3
