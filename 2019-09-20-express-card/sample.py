#!/usr/bin/env python3

import numpy as np

def area_frac(d, N):
    total = 0
    hits = 0
    points = 2 * np.random.random((N, 2)) - 1
    d1 = np.linalg.norm(points, axis=1)
    d2 = np.linalg.norm(points - np.array((0, d)), axis=1)
    total = np.count_nonzero(d1 < 1)
    hits = np.count_nonzero((d1 < 1) & (d2 < 1))
    return hits / total

print(area_frac(.8079575, int(1e6)))
