#!/usr/bin/env python3

import math
import numpy as np

'''
n is number of sides

a is triangle base, b is triangle height
h is pyramid height
d is distance from midpoint of triangle base to center of pyramid base

Volume of the pyramid is nadh/6
d = a / (2 tan (pi/n))
h^2 = b^2 - d^2
'''

def V(n, a, b):
    d = a / 2 / math.tan(math.pi / n)
    h_squared = b**2 - d**2
    if h_squared <= 0:
        return math.nan
    h = math.sqrt(b**2 - d**2)
    return n * a * d * h / 6

def sweep(a, b):
    n = 3
    v = []
    while True:
        v_n = V(n, a, b)
        if math.isnan(v_n):
            break
        v.append(v_n)
        n += 1
    n_opt = np.argmax(v) + 3
    v_opt = np.max(v)
    return n_opt, v_opt

def example_triangle():
    a = 1
    b = a / 2 / math.tan(30 / 2 * math.pi / 180)
    return a, b

print(sweep(*example_triangle()))
