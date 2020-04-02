#!/usr/bin/env python3

import math
import random
import itertools
import numpy as np
import enum
from collections import deque

class Barbers(enum.Enum):
    TIFFANY = 0
    B1 = 1
    B2 = 2
    B3 = 3

def forward(line, waiting_for_tiffany, barber):
    if barber == Barbers.TIFFANY:
        if waiting_for_tiffany > 0:
            waiting_for_tiffany -= 1
        else:
            line.popleft()
    else:
        while line and line[0] == Barbers.TIFFANY:
            waiting_for_tiffany += 1
            line.popleft()
        if line:
            line.popleft()
    return line, waiting_for_tiffany


def push_new(line, waiting_for_tiffany):
    line.append(random.choice(list(Barbers)))
    return line, waiting_for_tiffany

line = deque()
waiting_for_tiffany = 0

for i in range(10):
    line, waiting_for_tiffany = push_new(line, waiting_for_tiffany)

total = 0
non_tiffanys = 0
for b in itertools.cycle(random.sample(list(Barbers), len(Barbers))):
    total += 1
    if waiting_for_tiffany == 0 and line[0] != Barbers.TIFFANY:
        non_tiffanys += 1

    if total % 100000 == 0:
        print(non_tiffanys, total, int(math.sqrt(total)), non_tiffanys / total)
    # print(b, [line[i].name for i in range(5)], waiting_for_tiffany)
    line, waiting_for_tiffany = forward(line, waiting_for_tiffany, b)
    while len(line) < 10:
        line, waiting_for_tiffany = push_new(line, waiting_for_tiffany)
