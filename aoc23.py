#!/usr/bin/env python3

from heapq import heappop, heappush
from operator import itemgetter
import sys


with open(sys.argv[1] if len(sys.argv) >= 2 else 'aoc23_input.txt') as f:
    input = f.read()

def parse_state(input):
    return (0,) * 7 + \
        tuple(map('.ABCD'.index, itemgetter(31, 33, 35, 37, 45, 47, 49, 51)(input)))


energy_table = (-1, 1, 10, 100, 1000)
is_empty = lambda state, *ls: all(state[l] == 0 for l in ls)
is_hallway = lambda a: a <= 6
is_own_room = lambda t, a: (a - 7) % 4 == t - 1
is_freed_room = lambda state, t: all(x in (0, t) for x in state[6 + t::4])
is_filled_below = lambda state, a: all(state[a + 4::4])

def generate_paths(roomsize=2):
    neighbors = (
        *((i, i+1) for i in range(6)),
        *((1+i, 7+i) for i in range(4)),
        *((2+i, 7+i) for i in range(4)),
        *((7+i+r*4, 7+i+(r+1)*4) for i in range(4) for r in range(roomsize-1)))
    neighbors = neighbors + tuple((b, a) for a, b in neighbors)
    paths = {(a, b): () for a, b in neighbors}
    for _ in range(5+roomsize):
        for (a, b), path in tuple(paths.items()):
            for c, d in neighbors:
                if b == c:
                    new_path = path + (b,)
                    if (a, d) not in paths or len(new_path) < len(paths[(a, d)]):
                        paths[a, d] = new_path
    for (a, b), path in tuple(paths.items()):
        if is_hallway(a) == is_hallway(b):
            del paths[(a, b)]
    return paths

def search(start, goal, expand):
    # A* looked promising here, but any gains were eaten up by extra effort
    # to calculate h(), so I removed it again.
    queue = [(0, start)]
    seen = set()
    while queue:
        cost, state = heappop(queue)
        if state == goal:
            return cost
        elif state not in seen:
            seen.add(state)
            for nextcost, nextstate in expand(cost, state):
                heappush(queue, (nextcost, nextstate))
    return None

def mkexpand(paths):
    def expand(cost, state):
        for (a, b), path in paths.items():
            if a >= len(state): print('state', state, a)
            if (t:=state[a]) and is_empty(state, b, *path):
                is_hw = is_hallway(a)
                is_fr = is_freed_room(state, t)
                if (is_hw and is_own_room(t, b) and is_fr and is_filled_below(state, b)) \
                        or (not is_hw and not (is_fr and is_own_room(t, a))):
                    temp = list(state)
                    temp[a], temp[b] = 0, temp[a]
                    newstate = tuple(temp)
                    newcost = cost + energy_table[t] * \
                        (len(path) + 1 + sum(1 for u in (a, *path, b) if 1 <= u <= 5))
                    yield newcost, newstate
    return expand


paths = generate_paths(roomsize=2)
start = parse_state(input)
goal = (0, 0, 0, 0, 0, 0, 0) + (1, 2, 3, 4) * 2
energy = search(start, goal, expand=mkexpand(paths))

print(f'Part 1: {energy=}')


paths2 = generate_paths(roomsize=4)
start2 = (*start[:11],  4, 3, 2, 1,  4, 2, 1, 3,  *start[11:])
goal2 = goal + (1, 2, 3, 4) * 2
energy2 = search(start2, goal2, expand=mkexpand(paths2))

print(f'Part 2: {energy2=}')
