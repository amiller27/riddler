#include <deque>
#include <iostream>
#include <random>

using Generator = std::minstd_rand;

bool next_in_line;
long waiting = 0;

std::bernoulli_distribution dist(0.25);

void push_new(Generator& rng) {
    next_in_line = dist(rng);
}

void forward(const int barber, Generator& rng) {
    if (barber == 0) {  // It's Tiffany
        if (waiting > 0)
            waiting--;
        else {
            push_new(rng);
        }
    } else {
        while (next_in_line == true) {
            waiting++;
            push_new(rng);
        }

        push_new(rng);
    }
}

int main() {
    Generator rng{std::random_device{}()};

    push_new(rng);

    long total = 0;
    long non_tiffanys = 0;

    while (true) {
        for (int i = 0; i < 4; i++) {
            total++;
            if (waiting == 0 && next_in_line != true) {
                non_tiffanys++;
            }

            if (total % long(1e8) == 0) {
                std::cout << non_tiffanys << " " << total << " "
                          << std::round(std::sqrt(total)) << " "
                          << non_tiffanys / double(total) << std::endl;
            }

            forward(i, rng);
        }
    }
}
