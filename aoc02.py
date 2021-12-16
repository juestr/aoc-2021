#!/usr/bin/env python3

from functools import reduce
from itertools import groupby
from operator import itemgetter

with open('aoc02_input.txt') as f:
    a2 = f.read().splitlines()


cmds = [((s:=cmd.split())[0], int(s[1])) for cmd in a2]
move_ctr = {cmd: sum(map(itemgetter(1), xs))
    for cmd, xs in groupby(sorted(cmds), key=itemgetter(0))}
position = move_ctr['forward']
depth = move_ctr['down'] - move_ctr['up']

print(f'Part 1: {position * depth=}')


def move(state, cmd):
    depth, pos, aim = state
    match cmd:
        case 'down', x: return (depth, pos, aim+x)
        case 'up', x: return (depth, pos, aim-x)
        case 'forward', x: return (depth + aim*x, pos+x, aim)

depth, position, _ = reduce(move, cmds, (0, 0, 0))

print(f'Part 2: {position * depth=}')
