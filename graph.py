from __future__ import annotations
from collections import defaultdict

import itertools as it

from graph_typing import VERTEX_T, ConnectivityMap


class Graph:
    """Define methods that are common to all graphs here."""

    vertices: list[VERTEX_T]
    connectivity_map: ConnectivityMap

    def add_edge(self, v1, v2):
        self.connectivity_map[v1] = v2
        assert self.connectivity_map[v2] == v1

    def distance(self, v1: VERTEX_T, v2: VERTEX_T) -> int:
        ...


class Hypercube(Graph):
    def __init__(self, n: int) -> None:
        CHOICES = (0, 1)
        self.vertices: list[VERTEX_T] = list(it.product(CHOICES, repeat=n))
        # gives the cartesian product {0, 1}^n as a list of tuples
        # ie. [(0, 0, 0), (0, 0, 1), (0, 1, 0), (0, 1, 1), (1, 0, 0), (1, 0, 1), (1, 1, 0), (1, 1, 1)], for n=3
