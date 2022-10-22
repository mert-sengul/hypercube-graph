from __future__ import annotations
from typing import Generic, Iterable, Type, TypeVar, Sequence

import unittest

from graph import Graph, ConnectivityMap, cycle_equal
import graph

_CT = TypeVar("_CT")


_KV = TypeVar("_KV")
_TV = TypeVar("_TV")


class TestGraph1(unittest.TestCase):
    def _setUpGraph_(self) -> None:
        "Override this method. Do not call with super()."
        self.graph.add_edge(0, 1)
        self.graph.add_edge(0, 2)
        self.graph.add_edge(1, 2)
        self.graph.add_edge(2, 0)
        self.graph.add_edge(2, 3)

    def _setUp_(self) -> None:
        "Override this method for other use cases. Do not call with super()."
        _GT = int
        self.graph: Graph[_GT] = Graph()
        self.expected_cmap_result: dict[_GT, set[_GT]] = {
            1: {0, 2},
            0: {1, 2},
            2: {0, 1, 3},
            3: {2},
        }
        self.expected_paths: set[tuple[_GT, ...]] = {(0, 1, 2, 3), (0, 2, 1), (0, 2, 3)}
        self.expected_conn_comps: set[frozenset[_GT]] = {frozenset({0, 1, 2, 3})}
        self.expected_distances_dict: dict[tuple[_GT, _GT], float] = {
            (0, 1): 1,
            (1, 3): 2,
        }

    def setUp(self) -> None:
        self._setUp_()
        self._setUpGraph_()
        self.graph.DFS()
        return super().setUp()

    def test_cmap(self):
        self.assertDictEqual(dict(self.graph.cmap.items()), self.expected_cmap_result)

    def test_conn_comps(self):
        self.assertSetEqual(self.graph.conn_comps, self.expected_conn_comps)

    def test_paths(self):
        print()
        print(self.graph.paths)
        print()

    def test_distance(self):
        res_dict = {}
        for u, v in self.expected_distances_dict:
            res_dict[(u, v)] = self.graph.distance(u, v)
        self.assertDictEqual(self.expected_distances_dict, res_dict)

    #     graph_paths = self.graph.paths.copy()
    #     expected_paths = self.expected_paths.copy()
    #     self.assertEqual(
    #         len(graph_paths),
    #         len(expected_paths),
    #         f"""Path counts do not equal: {len(graph_paths)=}, {len(expected_paths)=}.
    #         {graph_paths=}
    #         {expected_paths=}""",
    #     )
    #     possible_matches: dict[tuple, list[list]] = {p: [] for p in graph_paths}
    #     for _path in graph_paths:
    #         self.assertTrue(
    #             any(
    #                 cycle_equal(_path, o_path := _o_path) for _o_path in expected_paths
    #             ),
    #             msg=f"{_path=} is not in {expected_paths}",
    #         )
    #         expected_paths.remove(o_path)

    #     # self.assertCountEqual(self.graph.paths, {(0, 1, 2, 3), (0, 2, 1), (0, 2, 3)})
    #     # self.assertEqual(len(self.graph.paths), len(self.expected_paths))


class TestGraph2(TestGraph1):
    def _setUpGraph_(self):
        adj_dict = {
            "5": ["3", "7"],
            "3": ["2", "4"],
            "7": ["8"],
            "2": [],
            "4": ["8"],
            "8": [],
        }
        for _v, _l in adj_dict.items():
            for _u in _l:
                self.graph.add_edge(_v, _u)

    def _setUp_(self):
        _GT = str
        self.graph: Graph[_GT] = Graph()
        self.expected_cmap_result: dict[_GT, set[_GT]] = {
            "3": {"2", "5", "4"},
            "5": {"7", "3"},
            "7": {"8", "5"},
            "2": {"3"},
            "4": {"8", "3"},
            "8": {"4", "7"},
        }
        self.expected_paths: set[tuple[_GT, ...]] = {
            ("7", "5", "3", "2"),
            ("7", "5", "3", "4", "8"),  #
            ("7", "8", "4", "3", "2"),
            ("7", "8", "4", "3", "5"),  # duplicate paths
        }
        self.expected_conn_comps: set[frozenset[_GT]] = {
            frozenset({"4", "2", "7", "8", "5", "3"})
        }
        self.expected_distances_dict: dict[tuple[_GT, _GT], float] = {
            ("2", "5"): 2,
            ("3", "5"): 1,
            ("2", "8"): 3,
            ("7", "4"): 2,
            ("3", "7"): 2,
        }


class TestGraph3(TestGraph1):
    def _setUpGraph_(self) -> None:
        adj_dict = {
            "5": ["3", "7"],
            "3": ["5"],
            "7": ["8"],
            "2": ["1"],
            "4": ["2"],
            "8": ["3"],
            "1": ["4"],
            "6": [],
        }

        for _v, _l in adj_dict.items():
            if not _l:
                self.graph.cmap[_v]
            for _u in _l:
                self.graph.add_edge(_v, _u)

    def _setUp_(self):
        _GT = str
        self.graph: Graph[_GT] = Graph()
        self.expected_cmap_result: dict[_GT, set[_GT]] = {
            "3": {"5", "8"},
            "5": {"7", "3"},
            "7": {"5", "8"},
            "8": {"7", "3"},
            "1": {"2", "4"},
            "2": {"4", "1"},
            "4": {"2", "1"},
            "6": set(),
        }
        self.expected_paths: set[tuple[_GT, ...]] = {
            ("4", "2", "1"),
            ("3", "8", "7", "5"),
            ("4", "1", "2"),
            ("3", "5", "7", "8"),
            ("6",),
        }
        self.expected_conn_comps: set[frozenset[_GT]] = {
            frozenset({"6"}),
            frozenset({"2", "4", "1"}),
            frozenset({"5", "7", "3", "8"}),
        }
        self.expected_distances_dict: dict[tuple[_GT, _GT], float] = {
            ("6", "5"): float("inf"),
            ("3", "4"): float("inf"),
            ("3", "7"): 2,
            ("3", "5"): 1,
            ("2", "4"): 1,
            ("3", "8"): 1,
        }


if __name__ == "__main__":
    unittest.main()
