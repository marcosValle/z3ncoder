#!/usr/bin/env python

from z3 import *
import argparse

def solve(b):
    x1 = Int('x1')
    x2 = Int('x2')
    x3 = Int('x3')
    x4 = Int('x4')
    y1 = Int('y1')
    y2 = Int('y2')
    y3 = Int('y3')
    y4 = Int('y4')
    z1 = Int('z1')
    z2 = Int('z2')
    z3 = Int('z3')
    z4 = Int('z4')
    X = Int('X')
    Y = Int('Y')
    Z = Int('Z')

    s = Solver()
    s.add(Or(X+Y+Z==b, X+Y+Z==0x100000000 + b))

    s.add(0x1000000*x1 + 0x10000*x2 + 0x100*x3 + x4 == X)
    s.add(0x1000000*y1 + 0x10000*y2 + 0x100*y3 + y4 == Y)
    s.add(0x1000000*z1 + 0x10000*z2 + 0x100*z3 + z4 == Z)

    s.add(x1>0x20, x1<0x80, x1!=0x0A, x1!=0x0D, x1!=0x2F, x1!=0x3A, x1!=0x3F)
    s.add(x2>0x20, x2<0x80, x2!=0x0A, x2!=0x0D, x2!=0x2F, x2!=0x3A, x2!=0x3F)
    s.add(x3>0x20, x3<0x80, x3!=0x0A, x3!=0x0D, x3!=0x2F, x3!=0x3A, x3!=0x3F)
    s.add(x4>0x20, x4<0x80, x4!=0x0A, x4!=0x0D, x4!=0x2F, x4!=0x3A, x4!=0x3F)
    s.add(y1>0x20, y1<0x80, y1!=0x0A, y1!=0x0D, y1!=0x2F, y1!=0x3A, y1!=0x3F)
    s.add(y2>0x20, y2<0x80, y2!=0x0A, y2!=0x0D, y2!=0x2F, y2!=0x3A, y2!=0x3F)
    s.add(y3>0x20, y3<0x80, y3!=0x0A, y3!=0x0D, y3!=0x2F, y3!=0x3A, y3!=0x3F)
    s.add(y4>0x20, y4<0x80, y4!=0x0A, y4!=0x0D, y4!=0x2F, y4!=0x3A, y4!=0x3F)
    s.add(z1>0x20, z1<0x80, z1!=0x0A, z1!=0x0D, z1!=0x2F, z1!=0x3A, z1!=0x3F)
    s.add(z2>0x20, z2<0x80, z2!=0x0A, z2!=0x0D, z2!=0x2F, z2!=0x3A, z2!=0x3F)
    s.add(z3>0x20, z3<0x80, z3!=0x0A, z3!=0x0D, z3!=0x2F, z3!=0x3A, z3!=0x3F)
    s.add(z4>0x20, z4<0x80, z4!=0x0A, z4!=0x0D, z4!=0x2F, z4!=0x3A, z4!=0x3F)

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
