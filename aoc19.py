#!/usr/bin/env python3

from functools import reduce
from itertools import product
import numpy as np

# with open('aoc19_example.txt') as f:
with open('aoc19_input.txt') as f:
    a19 = f.read().splitlines()


Rot_x = np.array([[1, 0, 0], [0, 0, -1], [0, 1, 0]])
Rot_y = np.array([[0, 0, 1], [0, 1, 0], [-1, 0, 0]])
Rot_z = np.array([[0, -1, 0], [1, 0, 0], [0, 0, 1]])
Rot_base = [np.eye(3), Rot_x, Rot_y, Rot_z]
Orientations = np.unique([reduce(np.matmul, rotations).astype(np.int_)
    for rotations in product(Rot_base, repeat=4)], axis=0)

def locate(beacons, beacons2):
    for beacons2_o in beacons2 @ Orientations:
        distances, counts = np.unique(
            (beacons[:, np.newaxis] - beacons2_o).reshape(-1, 3),
            axis=0, return_counts=True)
        maxcount_idx = np.argmax(counts)
        if counts[maxcount_idx] >= 12:
            s2loc = distances[maxcount_idx]
            s2beacons = beacons2_o + s2loc
            return s2loc, s2beacons

# input transform
scanner_data = []
for line in a19:
    if line.startswith('---'):
        scanner = []
        scanner_data.append(scanner)
    elif line:
        scanner.append([float(x) for x in line.split(',')])
scanner_data = [np.array(scanner, dtype=np.int_) for scanner in scanner_data]

# initial state with scanner[0]
scanner_locs = [np.zeros(3)]
beacons = [scanner_data[0]]
unlocated = list(range(1, len(scanner_data)))

# locate all other scanners
for s1idx in range(len(scanner_data) - 1):
    assert s1idx < len(scanner_locs), 'stuck without progress'
    s1beacons = beacons[s1idx]
    for s2idx in unlocated[:]:
        match locate(s1beacons, scanner_data[s2idx]):
            case s2loc, s2beacons:
                print('matching', s1idx, s2idx)
                unlocated.remove(s2idx)
                scanner_locs.append(s2loc)
                beacons.append(s2beacons)

all_beacons = np.unique(np.vstack(beacons), axis=0).shape[0]

print(f'Part 1: {all_beacons=}')

locs = np.array(scanner_locs, dtype=np.int_)
distances = np.sum(np.abs(locs[:, np.newaxis] - locs).reshape(-1, 3), axis=1)
max_distance = np.max(distances)

print(f'Part 2: {max_distance=}')
