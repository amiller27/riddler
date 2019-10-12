#!/usr/bin/env python3

from decimal import Decimal
import math
import matplotlib.pyplot as plt
import numpy as np

def p2(m, n):
    '''
    Probability of having m days two-to-a-day and n days one-to-a-day,
    given that we have 2m+n people total
    '''
    if not math.isnan(cache[m, n]):
        return cache[m, n]
    if m < 0 or n < 0:
        return 0
    if m == 0 and n == 1:
        return 1
    cache[m, n] = (p2(m - 1, n + 1) * ((n + 1) / Decimal(365))
                   + p2(m, n - 1) * ((365 - m - (n - 1)) / Decimal(365)))
    return cache[m, n]

def p3(N):
    '''
    Probability that we have N people, with no 3 on the same day
    '''
    return sum(p2(i // 2, N - i) for i in range(0, N + 1, 2))

MAX_N = 100
cache = np.tile(Decimal(np.NaN), (MAX_N // 2 + 1, MAX_N + 1))

plt.plot([p3(N) for N in range(1, MAX_N)])
plt.plot([0.5 for _ in range(1, MAX_N)])
plt.show()
