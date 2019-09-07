#!/usr/bin/env python3

import enum
import random


class Outcome(enum.Enum):
    WIN = enum.auto()
    LOSE = enum.auto()


def roll_game(prng, prob_win_point, is_tiebreak):
    my_score = 0
    their_score = 0

    winning_points = 7 if is_tiebreak else 4

    while True:
        if my_score >= winning_points and my_score - their_score >= 2:
            return Outcome.WIN
        if their_score >= winning_points and their_score - my_score >= 2:
            return Outcome.LOSE

        if prng() < prob_win_point:
            my_score += 1
        else:
            their_score += 1


def roll_set(prng, prob_win_point):
    my_games = 0
    their_games = 0

    while True:
        if my_games == 6 and their_games == 6:
            return roll_game(prng, prob_win_point, True)
        if my_games >= 6 and my_games - their_games >= 2:
            return Outcome.WIN
        if their_games >= 6 and their_games - my_games >= 2:
            return Outcome.LOSE

        if roll_game(prng, prob_win_point, False) == Outcome.WIN:
            my_games += 1
        else:
            their_games += 1


def roll_match(prng, prob_win_point, is_mens):
    my_sets = 0
    their_sets = 0

    winning_sets = 3 if is_mens else 2

    while True:
        if my_sets == winning_sets:
            return Outcome.WIN
        if their_sets == winning_sets:
            return Outcome.LOSE

        if roll_set(prng, prob_win_point) == Outcome.WIN:
            my_sets += 1
        else:
            their_sets += 1


def get_win_prob(f):
    matches = 0
    wins = 0

    while True:
        matches += 1
        wins += 1 if f() == Outcome.WIN else 0
        if matches % 100000 == 0:
            alpha = wins
            beta = matches - wins
            var = alpha * beta / (alpha + beta) ** 2 / (alpha + beta + 1)
            stddev = var ** 0.5
            print("{}/{}\t{:.8f}\t+-{}".format(wins, matches, wins / matches, stddev))


def disk_iterator():
    with open("random.txt") as f:
        for line in f.readlines():
            if line.strip():
                yield float(line.strip())


if __name__ == "__main__":
    prng_iter = disk_iterator()
    disk_prng = lambda: next(prng_iter)

    dev_prng = lambda: random.random()

    get_win_prob(lambda: roll_match(dev_prng, 0.55, True))
