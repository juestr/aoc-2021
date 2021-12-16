#!/usr/bin/env python3

from collections import namedtuple
from itertools import islice
from math import prod
from operator import lt, gt, eq


with open('aoc16_input.txt') as f:
    a16 = f.read()
input = islice(bin(int(a16, 16)), 2, None)


Packet = namedtuple('Packet', 'kind version pid bits payload')

def take_int(w):
    return w and int(''.join(islice(input, w)), 2)

def parse_packet():
    v = take_int(3)
    pid = take_int(3)
    match pid:
        case 4: return parse_literal(v, pid)
        case x: return parse_op(v, pid)

def parse_literal(v, pid):
    groups = 1
    val = 0
    while (cont:=take_int(1)):
        groups += 1
        val = (val << 4) | take_int(4)
    val = (val << 4) | take_int(4)
    return Packet('lit', v, pid, 6 + groups * 5, val)

def parse_op(v, pid):
    lentype = take_int(1)
    if lentype:
        npkts = take_int(11)
        subpkts = tuple(parse_packet() for _ in range(npkts))
        subbits = sum(bits for (_, _, _, bits, *_) in subpkts)
        return Packet('op', v, pid, 18 + subbits, subpkts)
    else:
        nbits = todo = take_int(15)
        subpkts = []
        while todo > 0:
            newpkt = (_, _, _, bits, *_) = parse_packet()
            subpkts.append(newpkt)
            todo -= bits
        assert todo == 0, 'subpackets size mismatch'
        return Packet('op', v, pid, 22 + nbits, tuple(subpkts))

def sum_versions(packet):
    match packet:
        case Packet('lit', v, _, _, _):  return v
        case Packet('op', v, _, _, xs):  return v + sum(map(sum_versions, xs))

top_packet = parse_packet()

print(f'Part 1: {sum_versions(top_packet)=}')


Ops = [sum, prod, min, max, None, gt, lt, eq]

def packet_eval(packet):
    match packet:
        case Packet('lit', _, _, _, val):
            return val
        case Packet('op', _, pid, _, xs):
            f, operands = Ops[pid], map(packet_eval, xs)
            return f(operands) if 0 <= pid <= 3 else f(*operands)

print(f'Part 2: {packet_eval(top_packet)=}')
