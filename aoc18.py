#!/usr/bin/env python3

from dataclasses import dataclass
from itertools import permutations

@dataclass(frozen=True)
class SFN:
    a: 'int | SFN'
    b: 'int | SFN'

    @staticmethod
    def from_list(l: list) -> 'SFN':
        return SFN(*(x if isinstance(x, int) else SFN.from_list(x) for x in l))

    def magnitude(self: 'int | SFN') -> int:
        match self:
            case int(i):    return i
            case SFN(a, b): return SFN.magnitude(a) * 3 + SFN.magnitude(b) * 2

    def __add__(self, other: 'SFN') -> 'SFN':

        def add_left(n: 'int | SFN', dmg: int | None) -> 'int | SFN':
            match dmg, n:
                case None, _:               return n
                case _, int(i):             return i + dmg
                case _, SFN(int(a), b):     return SFN(a + dmg, b)
                case _, SFN(SFN() as a, b): return SFN(add_left(a, dmg), b)

        def add_right(n: 'int | SFN', dmg: int | None) -> 'int | SFN':
            match dmg, n:
                case None, _:               return n
                case _, int(i):             return i + dmg
                case _, SFN(a, int(b)):     return SFN(a, b + dmg)
                case _, SFN(a, SFN() as b): return SFN(a, add_right(b, dmg))

        def explode_nested(n: 'SFN', lvl: int=4) -> tuple['SFN', int, int] | None:
            match lvl, n:
                case 0, SFN(a, b):
                    return 0, a, b
                case 0, _:
                    return None
                case _, SFN(SFN() as a, b) if r:=explode_nested(a, lvl - 1):
                    new_a, dmg_left, dmg_right = r
                    return SFN(r[0], add_left(b, r[2])), r[1], None
                    return SFN(new_a, add_left(b, dmg_right)), dmg_left, None
                case _, SFN(a, SFN() as b) if r:=explode_nested(b, lvl - 1):
                    new_b, dmg_left, dmg_right = r
                    return SFN(add_right(a, dmg_left), new_b), None, dmg_right
                case _:
                    return None

        def split_ge10(n: 'int | SFN') -> tuple['SFN'] | None:
            match n:
                case int(a) if a > 9:                return SFN(a // 2, (a+1) // 2),
                case SFN(a, b) if r:=split_ge10(a):  return SFN(r[0], b),
                case SFN(a, b) if r:=split_ge10(b):  return SFN(a, r[0]),
                case _:                              return None

        n = SFN(self, other)
        while r:=(explode_nested(n) or split_ge10(n)):
            n, *_ = r
        return n

    def __radd__(self, other) -> 'SFN':
        assert other == 0
        return self

    def __str__(self) -> str:
        return f'[{self.a}, {self.b}]'


with open('aoc18_input.txt') as f:
    a17 = f.read().splitlines()

numbers = [SFN.from_list(eval(l, {})) for l in a17]
result = sum(numbers).magnitude()

print(f'Part 1: {result=}')


max_magnitude = max((a + b).magnitude() for a, b in permutations(numbers, 2))

print(f'Part 2: {max_magnitude=}')
