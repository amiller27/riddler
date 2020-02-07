#include <array>
#include <deque>
#include <exception>
#include <iostream>
#include <vector>

constexpr const size_t SIZE = 10;
std::array<std::array<int, SIZE>, SIZE> maze = {std::array<int, SIZE>{6, 2, 1, 3, 6, 1, 7, 7, 4, 3},
                                                std::array<int, SIZE>{2, 3, 4, 5, 7, 8, 1, 5, 2, 3},
                                                std::array<int, SIZE>{1, 6, 1, 2, 5, 1, 6, 3, 6, 2},
                                                std::array<int, SIZE>{5, 3, 5, 5, 1, 6, 7, 3, 7, 3},
                                                std::array<int, SIZE>{1, 2, 6, 4, 1, 3, 3, 5, 5, 5},
                                                std::array<int, SIZE>{2, 4, 6, 6, 6, 2, 1, 3, 8, 8},
                                                std::array<int, SIZE>{2, 4, 0, 2, 3, 6, 5, 2, 4, 6},
                                                std::array<int, SIZE>{3, 1, 7, 6, 2, 3, 1, 5, 7, 7},
                                                std::array<int, SIZE>{6, 1, 3, 6, 4, 5, 4, 2, 2, 7},
                                                std::array<int, SIZE>{6, 7, 5, 7, 6, 2, 4, 1, 9, 1}};

struct P {
    int i;
    int j;

    bool operator==(const auto& rhs) const {
        return i == rhs.i && j == rhs.j;
    }

    friend std::ostream& operator<<(std::ostream& stream, const auto& p) {
        stream << p.i << " " << p.j;
        return stream;
    }
};

std::vector<P> s(const P& p) {
    std::vector<P> results;
    for (int jprime = 0; jprime < SIZE; jprime++) {
        if (jprime == p.j) continue;

        if (maze[p.i][jprime] == std::abs(jprime - p.j)) {
            results.push_back({p.i, jprime});
        }
    }

    for (int iprime = 0; iprime < SIZE; iprime++) {
        if (iprime == p.i) continue;

        if (maze[iprime][p.j] == std::abs(iprime - p.i)) {
            results.push_back({iprime, p.j});
        }
    }

    return results;
}

void print_path(const auto& backp) {
    P curr {SIZE - 1, 0};
    while (maze[curr.i][curr.j] != 0) {
        std::cout << curr << std::endl;
        curr = backp[curr.i][curr.j];
    }
    std::cout << curr << std::endl;
}

int main() {
    std::array<std::array<bool, SIZE>, SIZE> closed;
    for (size_t i = 0; i < SIZE; i++) {
        for (size_t j = 0; j < SIZE; j++) {
            closed[i][j] = false;
        }
    }

    std::array<std::array<P, SIZE>, SIZE> backp;
    for (size_t i = 0; i < SIZE; i++) {
        for (size_t j = 0; j < SIZE; j++) {
            backp[i][j] = {-1, -1};
        }
    }

    std::deque<P> open;
    open.push_back({6, 2});

    if (maze[open.front().i][open.front().j] != 0) {
        throw std::runtime_error("Wrong start");
    }

    while (!open.empty()) {
        const auto p = open.front();
        open.pop_front();

        if (p == P{SIZE - 1, 0}) {
            print_path(backp);
            return 0;
        }

        for (const auto& pprime : s(p)) {
            if (!closed[pprime.i][pprime.j]) {
                open.push_back(pprime);
                backp[pprime.i][pprime.j] = p;
            }
            closed[pprime.i][pprime.j] = true;
        }
    }

    return 1;
}
