#!/usr/bin/env python3

import numpy as np

import warlord

solutions3 = warlord.load('../fivethirtyeight_data/riddler-castles/castle-solutions-3.csv')
solutions3 = solutions3[np.sum(solutions3, axis=1) == 100]
print(solutions3.shape)

submission = np.loadtxt('submission.txt')
submission_index = np.argwhere(np.all(solutions3 == submission, axis=1))[0, 0]

wins = warlord.win_stats(solutions3, solutions3)
ordering = np.argsort(wins)

top5 = ordering[-5:]
for i in reversed(range(5)):
    print(f'{top5[i]}\t{wins[top5[i]]}\t{solutions3[top5[i]]}')

print(f'Me: {np.argwhere(ordering == submission_index)}, {wins[submission_index]}')
