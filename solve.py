#!/usr/bin/env python

from z3 import *
import argparse

def solve(b):
    s = Solver()
    bad_chars = [ 0x20, 0x80, 0x0A, 0x0D, 0x2F, 0x3A, 0x3F ]
    x, y, z = BitVecs('x y z', 32)
    variables = [x, y, z]

    for var in variables:
        for k in range(0, 32, 8):
            s.add(Extract(k+7, k, var) > BitVecVal(0x20, 8))
            s.add(ULT(Extract(k+7, k, var), BitVecVal(0x80, 8)))
            for c in bad_chars:
                s.add(Extract(k+7, k, var) != BitVecVal(c, 8))

    s.add(x+y+z==b)

    s.check()
    s.model()
    r = []
    for i in s.model():
        r.append(s.model()[i].as_long())

    return r

parser = argparse.ArgumentParser()
parser.add_argument("-a", "--addr", type=lambda x: (int(x,16)),
        help="Address to carve")
args = parser.parse_args()

if not args.addr:
    parser.print_help()
    parser.exit()

n = args.addr
neg = 0xFFFFFFFF - n + 1

print("Solving for 0x{:x}".format(n))
print("0xFFFFFFFF - 0x{:x} + 1 = 0x{:x}".format(n, neg)) #carry
res = solve(neg)

print('###########')
sumCheck = 0
for b in res[-3:]:
    sumCheck += b
    print(hex(b))
print('###########')

print('Check sum = {}'.format(hex(sumCheck)))
