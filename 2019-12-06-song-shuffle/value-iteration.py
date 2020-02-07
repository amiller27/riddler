#!/usr/bin/env python3

import decimal
import math
import numpy as np

def k(N):
    bellman_eps = 1e-10
    V = np.arange(N, dtype=decimal.Decimal)
    while True:

        new_V = decimal.Decimal(1) + np.minimum(np.roll(V, 1), sum(V, decimal.Decimal(0)) / decimal.Decimal(N))
        new_V[0] = decimal.Decimal(0)
        if np.all(np.abs(V - new_V) < bellman_eps):
            break
        V = new_V
    for i in range(N):
        if V[i] < i:
            return V, i - 1

def vtwiddle(N, k):
    return N/(k+1) + k/2

def argmin_vtwiddle(N):
    k = (2*N)**0.5 - 1
    k1 = math.floor(k)
    k2 = math.ceil(k)
    return k1 if vtwiddle(N, k1) < vtwiddle(N, k2) else k2


for N in range(1, 101):
    vi_k = k(N)
    analytic_k = argmin_vtwiddle(N)
    print(N, vi_k, analytic_k, vi_k == analytic_k)

print('Answer:', argmin_vtwiddle(100))
print('Average presses:', np.mean(k(100)[0]))
