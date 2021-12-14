#!/usr/bin/env python3

from itertools import chain, pairwise
import numpy as np


with open('aoc14_input.txt') as f:
    a14iter = iter(f.read().splitlines())

start, _ = next(a14iter), next(a14iter)
rules = [(x[0], x[1], x[6]) for x in a14iter]

materials = sorted(set(chain(start, chain.from_iterable(rules))))
N = len(materials)

# pairs are encoded as a single int from combining indices into material
start_pairs = np.zeros(N * N, dtype=np.int_)
for a, b in pairwise(map(materials.index, start)):
    start_pairs[a*N + b] += 1

# The expansion matrix is indexed on both sides by all possible pairs
# of materials. Row i contains 1 in columns for pairs replacing pair i.
expansion = np.identity(N*N, dtype=np.int_)
for abc in rules:
    a, b, c = map(materials.index, abc)
    i = a*N + b
    expansion[i, i] = 0
    expansion[i, a*N + c] = 1
    expansion[i, c*N + b] = 1

def expanded_peak2peak(steps):
    expanded_pairs = start_pairs @ np.linalg.matrix_power(expansion, steps)
    material_counts = np.sum(expanded_pairs.reshape((N, N)), axis=1)
    material_counts[materials.index(start[-1])] += 1
    return np.ptp(material_counts)


step10 = expanded_peak2peak(10)
print(f'Part 1: {step10=}')

step40 = expanded_peak2peak(40)
print(f'Part 2: {step40=}')
