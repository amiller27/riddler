#!/usr/bin/env python3

import sympy


def get_prob_win_game(
    prob_win_point, my_score, their_score, is_tiebreaker, cache, equations
):
    if (my_score, their_score) in cache.keys():
        return cache[(my_score, their_score)]

    var = sympy.symbols("pg{}_{}".format(my_score, their_score))
    cache[(my_score, their_score)] = var

    winning_score = 7 if is_tiebreaker else 4

    if my_score >= winning_score and their_score >= winning_score:
        if my_score - their_score == 1:
            # my ad
            result = prob_win_point * 1 + (1 - prob_win_point) * get_prob_win_game(
                prob_win_point,
                my_score - 1,
                their_score,
                is_tiebreaker,
                cache,
                equations,
            )
        elif my_score - their_score == 0:
            # deuce
            result = prob_win_point * get_prob_win_game(
                prob_win_point,
                my_score + 1,
                their_score,
                is_tiebreaker,
                cache,
                equations,
            ) + (1 - prob_win_point) * get_prob_win_game(
                prob_win_point,
                my_score,
                their_score + 1,
                is_tiebreaker,
                cache,
                equations,
            )
        elif my_score - their_score == -1:
            # their ad
            result = (
                prob_win_point
                * get_prob_win_game(
                    prob_win_point,
                    my_score,
                    their_score - 1,
                    is_tiebreaker,
                    cache,
                    equations,
                )
                + (1 - prob_win_point) * 0
            )
        else:
            assert False
    elif my_score >= winning_score and my_score - their_score >= 2:
        result = 1
    elif their_score >= winning_score and their_score - my_score >= 2:
        result = 0
    else:
        result = prob_win_point * get_prob_win_game(
            prob_win_point, my_score + 1, their_score, is_tiebreaker, cache, equations
        ) + (1 - prob_win_point) * get_prob_win_game(
            prob_win_point, my_score, their_score + 1, is_tiebreaker, cache, equations
        )

    equations.append(sympy.Eq(var, result))
    return var


def get_prob_win_set(prob_win_game, prob_win_tiebreak, my_score, their_score, cache):
    if (my_score, their_score) in cache.keys():
        return cache[(my_score, their_score)]

    if my_score == 6 and their_score == 6:
        result = prob_win_tiebreak
    elif my_score >= 6 and my_score - their_score >= 2:
        return 1
    elif their_score >= 6 and their_score - my_score >= 2:
        return 0
    else:
        result = prob_win_game * get_prob_win_set(
            prob_win_game, prob_win_tiebreak, my_score + 1, their_score, cache
        ) + (1 - prob_win_game) * get_prob_win_set(
            prob_win_game, prob_win_tiebreak, my_score, their_score + 1, cache
        )

    cache[(my_score, their_score)] = sympy.simplify(result)
    return result


def get_prob_win_match(prob_win_set, is_mens, my_score, their_score):
    required_sets = 3 if is_mens else 2

    if my_score == required_sets:
        return 1
    if their_score == required_sets:
        return 0
    return sympy.simplify(
        prob_win_set
        * get_prob_win_match(prob_win_set, is_mens, my_score + 1, their_score)
        + (1 - prob_win_set)
        * get_prob_win_match(prob_win_set, is_mens, my_score, their_score + 1)
    )


def compute_prob_win(prob_win_point, is_mens):
    game_variables = {}
    game_equations = []
    prob_win_game_var = get_prob_win_game(
        prob_win_point, 0, 0, False, game_variables, game_equations
    )
    game_variables_list = list(game_variables.values())
    prob_win_game_solution = sympy.linsolve(game_equations, game_variables_list)
    assert prob_win_game_solution.is_FiniteSet
    prob_win_game = list(prob_win_game_solution)[0][
        game_variables_list.index(prob_win_game_var)
    ]
    print("Game win prob:", prob_win_game)
    if not USE_SYMBOLIC_P:
        print("Approx:", float(prob_win_game))

    tiebreak_variables = {}
    tiebreak_equations = []
    prob_win_tiebreak_var = get_prob_win_game(
        prob_win_point, 0, 0, True, tiebreak_variables, tiebreak_equations
    )
    tiebreak_variables_list = list(tiebreak_variables.values())
    prob_win_tiebreak_solution = sympy.linsolve(
        tiebreak_equations, tiebreak_variables_list
    )
    assert prob_win_tiebreak_solution.is_FiniteSet
    prob_win_tiebreak = list(prob_win_tiebreak_solution)[0][
        tiebreak_variables_list.index(prob_win_tiebreak_var)
    ]
    print("Tiebreak win prob:", prob_win_tiebreak)
    if not USE_SYMBOLIC_P:
        print("Approx:", float(prob_win_tiebreak))

    prob_win_set = get_prob_win_set(prob_win_game, prob_win_tiebreak, 0, 0, {})
    print("Set win prob:", prob_win_set)
    if not USE_SYMBOLIC_P:
        print("Approx:", float(prob_win_set))

    return get_prob_win_match(prob_win_set, is_mens, 0, 0)


if __name__ == "__main__":
    USE_SYMBOLIC_P = False

    if USE_SYMBOLIC_P:
        prob_win_point = sympy.symbols("p")
    else:
        prob_win_point = sympy.Rational("55/100")

    men_win_prob = compute_prob_win(prob_win_point, True)
    print("Men's probability of win:", men_win_prob)
    if not USE_SYMBOLIC_P:
        print("Approx:", float(men_win_prob))
    print("Tournament win prob:", men_win_prob ** 7)
    if not USE_SYMBOLIC_P:
        print("Approx:", float(men_win_prob ** 7))

    women_win_prob = compute_prob_win(prob_win_point, False)
    print("Women's probability of win:", women_win_prob)
    if not USE_SYMBOLIC_P:
        print("Approx:", float(women_win_prob))
    print("Tournament win prob:", women_win_prob ** 7)
    if not USE_SYMBOLIC_P:
        print("Approx:", float(women_win_prob ** 7))
