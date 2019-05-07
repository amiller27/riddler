#!/usr/bin/env python3

import csv
import numba
import numpy as np
import random
import time


def load(filename):
    results = []
    with open(filename) as f:
        i = iter(csv.reader(f))
        next(i)
        for l in i:
            try:
                results.append(list(map(int, l[:10])))
            except BaseException:
                print('Failed to parse line', l)
        return np.array(results).astype(np.uint8)


def load538():
    return (load('../fivethirtyeight_data/riddler-castles/castle-solutions.csv'),
            load('../fivethirtyeight_data/riddler-castles/castle-solutions-2.csv'))


PERTURB_DECAY = 0.1


@numba.njit()
def perturb(pi):
    while True:
        i = random.randint(0, 9)
        if pi[i] != 0:
            j = random.randint(0, 9)
            pi[i] -= 1
            pi[j] += 1
            break
    if random.random() > PERTURB_DECAY:
        return perturb(pi)
    else:
        return pi


def play(a, b):
    '''
    Play strategies a against strategies b

    :param a: np.ndarray<int>, shape (n, 10)
    :param b: np.ndarray<int>, shape (m, 10)
    :returns wins: np.ndarray<bool>, shape (n, m), true if a wins
    '''
    start = time.time()
    result = _play(a, b)
    end = time.time()
    # print('Play time:', end - start)
    return result


@numba.njit(parallel=True)
def _play(a, b):
    result = np.empty((a.shape[0], b.shape[0]), dtype=np.uint8)
    for i in numba.prange(a.shape[0]):
        for j in range(b.shape[0]):
            a_points = 0
            b_points = 0
            for k in range(10):
                if a[i, k] < b[j, k]:
                    b_points += k + 1
                elif a[i, k] > b[j, k]:
                    a_points += k + 1
            result[i, j] = a_points > b_points
    return result


# Less accelerated version (by a ton)
#@numba.jit()
# def _play(a, b):
#    points = np.array(list(range(1, 11)), dtype=np.uint8)
#    a_wins = np.expand_dims(a, 1) > b
#    b_wins = np.expand_dims(a, 1) < b
#    # ties = (np.expand_dims(a, 1) == b).astype(int)
#    a_points = np.sum(a_wins * points  # + ties * points * 0.5
#                      , axis=-1)
#    b_points = np.sum(b_wins * points  # + ties * points * 0.5
#                      , axis=-1)
#    return a_points > b_points


def win_stats(a, b):
    '''
    Calculate wins for each policy in a against the dataset b
    '''
    win_table = play(a, b)
    wins = np.count_nonzero(win_table, axis=-1)
    return wins


def evolve(gene_pool, dataset, k_frac=0.25):
    wins = win_stats(gene_pool, dataset)
    top_k = np.argsort(wins)[-int(k_frac * gene_pool.shape[0]):]
    children = np.array([perturb(pi.copy())
                         for pi in gene_pool[top_k]
                         for _ in range(int(1 / k_frac))])

    top10 = np.argsort(wins)[-10:]
    print('Best 10:', gene_pool[top10])
    print('Scores:', wins[top10] / dataset.shape[0])

    return children


def kill_unfit(dataset, desired_size, split_frac=0.8):
    wins = win_stats(dataset, dataset)

    ordering = np.argsort(wins)
    bottom_split = ordering[:int(dataset.shape[0] * split_frac)]
    top_split = ordering[int(dataset.shape[0] * split_frac):]

    bottom_list = bottom_split.tolist()
    random.shuffle(bottom_list)

    bottom_cutoff = desired_size - top_split.shape[0]
    if bottom_cutoff < 0:
        raise ValueError('Desired size is incompatible with split fraction')

    living_indices = np.concatenate(
        (bottom_list[:bottom_cutoff], top_split))
    return dataset[living_indices]


def drift(gene_pool, dataset, iters=100):
    gene_pool = gene_pool.copy()
    dataset = dataset.copy()
    for i in range(iters):
        print('Iteration', i)
        print('Dataset size:', dataset.shape[0])
        print('Gene pool size:', gene_pool.shape[0])

        start = time.time()
        children = evolve(gene_pool, dataset)
        etime = time.time()
        dataset = kill_unfit(
            np.concatenate(
                (dataset, gene_pool)), dataset.shape[0])
        killtime = time.time()

        print(
            'Evolve time: {}, Kill time: {}'.format(
                etime - start,
                killtime - etime))

        gene_pool = children
    return gene_pool, dataset


if __name__ == '__main__':
    solutions1, solutions2 = load538()

    gene_pool = solutions2.copy()
    dataset = np.concatenate((solutions1, solutions2))
    drift(gene_pool, dataset)
