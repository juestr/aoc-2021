#!/usr/bin/env python3

import numpy as np
from scipy.sparse import csr_matrix, lil_matrix
from scipy.sparse.csgraph import breadth_first_order


with open('aoc09_input.txt') as f:
    a9 = np.genfromtxt(f, delimiter=1, dtype=np.int8)
#print(a9)


def neighbors_apply(f, a, acc=tuple, fill=0):
    rows, cols = a.shape
    fillh = np.repeat(fill, rows).reshape((1, rows))
    fillv = fillh.reshape((cols, 1))
    down =  np.concatenate(( f(a[:-1, :], a[1:, :]), fillh ), 0)
    up =    np.concatenate(( fillh, f(a[1:, :], a[:-1, :]) ), 0)
    right = np.concatenate(( f(a[:, :-1], a[:, 1:]), fillv ), 1)
    left =  np.concatenate(( fillv, f(a[:, 1:], a[:, :-1]) ), 1)
    return acc((down, up, right, left))

lows = neighbors_apply(np.less, a9, acc=np.logical_and.reduce, fill=True)
risk = np.sum((a9+1) * lows)

print(f'Part 1: {risk=}')


a9_not9 = (a9 != 9)
flows4d = [flow & a9_not9 for flow in neighbors_apply(np.greater, a9, fill=False)]
graph = lil_matrix((a9.size, a9.size), dtype=np.int8)
for offs, flow in zip((a9.shape[1], -a9.shape[1], 1, -1), flows4d):
    nodes = np.flatnonzero(flow)
    graph[nodes+offs, nodes] = 1  # reverse because we follow the flow upwards
graph = csr_matrix(graph)

basin = lambda low: breadth_first_order(graph, low, return_predecessors=False)
basins = [len(basin(low)) for low in np.flatnonzero(lows)]
largest = sorted(basins, reverse=True)[:3]
result = np.multiply.reduce(largest)

print(f'Part 2: {result=} {largest=}')
