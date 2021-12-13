#!/usr/bin/env python3

with open('aoc12_input.txt') as f:
    a12 = [l.split('-') for l in f.read().splitlines()]
# print(a12)


caves = {cave for conn in a12 for cave in conn}
bigcaves = frozenset(filter(str.isupper, caves))
connections = {c: {pair[pair[0]==c] for pair in a12 if c in pair} for c in caves}

def df_enum_paths(cave, visited_small=frozenset(), revisit_small=False):
    if cave == 'end':
        yield 1
    else:
        if cave not in bigcaves:
            visited_small = visited_small | {cave}
        for c in connections[cave] - visited_small:
            yield from df_enum_paths(c, visited_small, revisit_small=revisit_small)
        if revisit_small:
            for c in (connections[cave] & visited_small) - {'start'}:
                yield from df_enum_paths(c, visited_small, revisit_small=False)

paths = sum(df_enum_paths('start'))
print(f'Part 1: {paths=}')

paths = sum(df_enum_paths('start', revisit_small=True))
print(f'Part 2: {paths=}')
