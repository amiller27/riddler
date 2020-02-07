#!/usr/bin/env python3

import functools

@functools.lru_cache(maxsize=100000)
def win(x, y):
    if x == 0:
        return True
    if y == 0:
        return True
    if x == y:
        return True

    for i in range(1, max(x, y) + 1):
        if i <= x:
            if win(x - i, y) is False:
                return True
            if i <= y:
                if win(x - i, y - i) is False:
                    return True
        if i <= y:
            if win(x, y - i) is False:
                return True
    return False

PRINT_ALL = False

for n in range(20, 31):
    for x in range(0, n + 1):
        y = n - x

        i_win = not win(x, y)

        if PRINT_ALL:
            print(x, y, win(x, y))
        else:
            if i_win:
                print(x, y)
