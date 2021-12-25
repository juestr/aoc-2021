#!/usr/bin/env python3

from itertools import cycle, count
import sys
import numpy as np


with open(sys.argv[1] if len(sys.argv) >= 2 else 'aoc25_input.txt') as f:
    input = f.read().splitlines()

chart = np.array([list(l) for l in input])
eastw = (chart == '>')
southw = (chart == 'v')

def move(tribe, axis):
    destination = np.roll(tribe, 1, axis=axis) & np.logical_not(eastw) & np.logical_not(southw)
    departure = np.roll(destination, -1, axis=axis)
    np.putmask(tribe, departure, 0)
    np.putmask(tribe, destination, 1)
    return departure

for steps in count(1):
    departure_e = move(eastw, 1)
    departure_s = move(southw, 0)
    if not np.any(departure_e) and not np.any(departure_s):
        break

print(f'Part 1: {steps=}')

print(f'Part 2: sleigh started')
