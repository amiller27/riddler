#!/usr/bin/env python3

import enum
import math
import random

DETECTION_PROB = 0.25
FRAC_TESTED = 0.05

class Bill(enum.Enum):
    REAL = 0
    FAKE = 1

def throw(m, n):
    bills = random.sample([Bill.REAL] * m + [Bill.FAKE] * n, int(math.ceil(FRAC_TESTED * (m + n))))
    for bill in bills:
        if bill == Bill.FAKE:
            if random.random() <= DETECTION_PROB:
                return True
    return False

def p(m, n):
    '''Probability that you're caught with m real bills and n counterfeit ones'''
    THROWS = 10000
    return sum(0 if throw(m, n) else 1 for _ in range(THROWS)) / THROWS

def E(m, n):
    return p(m, n) * (m + n) * 100

def main():
    import matplotlib.pyplot as plt
    M = 25
    N = list(range(14, 100, 20))
    e = [E(M, n) for n in N]
    plt.plot(N, e)
    plt.show()

if __name__ == '__main__':
    main()
