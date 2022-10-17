from __future__ import annotations

from itertools import chain, combinations

import numpy as np
import numpy.typing as npt
from scipy.sparse.csgraph import connected_components



# represent each vertex with an N-tuple (a_1, a_2, a_3, a_4), where a_i is in {0, 1}.

def get_unit_vectors(N: int) -> list[npt.NDArray[np.int64]]:
    unit_vectors = []
    for i in range(N):
        v = np.zeros(shape=N, dtype=np.int64)
        v[i] = 1
        unit_vectors.append(v)
    return unit_vectors


def powerset(iterable: list[npt.NDArray[np.int64]]):
    "powerset([1,2,3]) --> () (1,) (2,) (3,) (1,2) (1,3) (2,3) (1,2,3)"
    s = list(iterable)
    return chain.from_iterable(combinations(s, r) for r in range(len(s)+1))

def get_cube_edges(N: int) -> list[npt.NDArray[np.int64]]:
    unit_vectors = get_unit_vectors(N)
    origin = np.zeros(shape=N, dtype=np.int64) # need this one for the empty set
    return [sum(subset)+origin if subset else origin for subset in powerset(unit_vectors)]

def get_cube_matrix(N: int):
    cube_edge_vectors = get_cube_edges(N)
    n_vertex = len(cube_edge_vectors)
    incidence_matrix = np.zeros(shape=(n_vertex,n_vertex), dtype=np.int64)
    for i in range(n_vertex):
        for j in range(n_vertex):
            vector1 = cube_edge_vectors[i]
            vector2 = cube_edge_vectors[j]
            if np.linalg.norm(vector1 - vector2, ord=1) == 1:
                incidence_matrix[i, j] = 1
    print(incidence_matrix)



if __name__ == "__main__":
    from pprint import pprint
    N = 4
    print("unit vecs:")
    pprint(get_unit_vectors(N))
    print("powerset:")
    pprint(list(powerset(get_unit_vectors(N))))
    print("cube edges:")
    pprint(get_cube_edges(N))
    m = get_cube_matrix(N)
    print(m)
    # connected_components(csgraph=m, directed=False)
