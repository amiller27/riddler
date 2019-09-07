#include <fstream>
#include <iomanip>
#include <iostream>
#include <random>

enum Outcome { WIN, LOSE };

Outcome roll_game(const auto prng,
                  const double prob_win_point,
                  const bool is_tiebreak) {
    if (is_tiebreak) {
        return prng() < .6541507671 ? Outcome::WIN : Outcome::LOSE;
    } else {
        return prng() < .623148502475 ? Outcome::WIN : Outcome::LOSE;
    }

    int my_score = 0;
    int their_score = 0;

    const int winning_points = is_tiebreak ? 7 : 4;

    while (true) {
        if (my_score >= winning_points && my_score - their_score >= 2) {
            return Outcome::WIN;
        }

        if (their_score >= winning_points && their_score - my_score >= 2) {
            return Outcome::LOSE;
        }

        if (prng() < prob_win_point) {
            my_score++;
        } else {
            their_score++;
        }
    }
}

Outcome roll_set(const auto prng, const double prob_win_point) {
    return prng() < .8150419926646 ? Outcome::WIN : Outcome::LOSE;
    int my_games = 0;
    int their_games = 0;

    while (true) {
        if (my_games == 6 && their_games == 6) {
            return roll_game(prng, prob_win_point, true);
        }

        if (my_games >= 6 && my_games - their_games >= 2) {
            return Outcome::WIN;
        }

        if (their_games >= 6 && their_games - my_games >= 2) {
            return Outcome::LOSE;
        }

        if (roll_game(prng, prob_win_point, false) == Outcome::WIN) {
            my_games++;
        } else {
            their_games++;
        }
    }
}

Outcome roll_match(const auto prng,
                   const double prob_win_point,
                   const bool is_mens) {
    int my_sets = 0;
    int their_sets = 0;

    const int winning_sets = is_mens ? 3 : 2;

    while (true) {
        if (my_sets == winning_sets) return Outcome::WIN;
        if (their_sets == winning_sets) return Outcome::LOSE;

        if (roll_set(prng, prob_win_point) == Outcome::WIN) {
            my_sets++;
        } else {
            their_sets++;
        }
    }
}

double get_win_prob(const auto f) {
    int matches = 0;
    int wins = 0;

    while (true) {
        matches++;
        if (f() == Outcome::WIN) wins++;
        if (matches % 100000 == 0) {
            const double alpha = wins;
            const double beta = matches - wins;
            const double var = (alpha * beta) / std::pow(alpha + beta, 2)
                               / (alpha + beta + 1);
            const double stddev = std::sqrt(var);
            std::cout << wins << "/" << matches << "\t" << std::setprecision(8)
                      << double(wins) / matches << "\t+-" << stddev
                      << std::endl;
        }
    }
}

int main() {
    std::random_device r{};
    std::mt19937 gen(r());
    std::uniform_real_distribution<> uniform{};
    auto dev_prng = [&gen, &uniform]() { return uniform(gen); };

    std::ifstream random_file("random.txt");
    auto disk_prng = [&random_file]() {
        double curr;
        if (random_file >> curr) return curr;
        throw std::runtime_error("Out of random numbers");
    };

    get_win_prob([&]() { return roll_match(dev_prng, 0.55, false); });
}
