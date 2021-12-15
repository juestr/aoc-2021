#!/usr/bin/env python3

import numpy as np
import scipy.sparse as sp

with open('aoc15_input.txt') as f:
    a15 = np.genfromtxt(f, delimiter=1, dtype=np.int8)
# print(a15)

def shortest_path_risk(cave):
    indices = np.arange(cave.size, dtype=np.intp).reshape(cave.shape)
    slice_a = slice(None), slice(None, -1)
    slice_b = slice(None), slice(1, None)
    graph = sp.lil_matrix((cave.size, cave.size), dtype=np.int8)
    for switchaxis in (tuple, lambda x: x[::-1]):
        part_a = cave[switchaxis(slice_a)].reshape(-1)
        part_b = cave[switchaxis(slice_b)].reshape(-1)
        idx_a = indices[switchaxis(slice_a)].reshape(-1)
        idx_b = indices[switchaxis(slice_b)].reshape(-1)
        graph[(idx_a, idx_b)] = part_b
        graph[(idx_b, idx_a)] = part_a
    from_first = sp.csgraph.dijkstra(graph, indices=(0,))[0]
    return int(from_first[-1])

risk = shortest_path_risk(a15)
print(f'Part 1: {risk=}')

blocks = [(a15 + (x - 1)) % 9 + 1 for x in range(9)]
cave2 = np.block([[blocks[x+y] for x in range(5)] for y in range(5)])
risk2 = shortest_path_risk(cave2)
print(f'Part 2: {risk2=}')
