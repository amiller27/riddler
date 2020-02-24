#include <array>
#include <chrono>
#include <iostream>

static constexpr const size_t T = 100;
static constexpr const size_t td = T + 1;
static constexpr const size_t xd = T * 2 * 2 + 1;
static constexpr const size_t x_mid = T * 2;

using Floating = float;

static constexpr const Floating half = 0.5;

void value_iterate(const std::array<Floating, xd>& v_tp1,
                   std::array<Floating, xd>& v_t,
                   const int layer_width) {
    for (int i = x_mid - layer_width; i <= x_mid + layer_width; i++) {
        const Floating v1 = (v_tp1[i + 1] + v_tp1[i - 1]);
        const Floating v2 = (v_tp1[i + 2] + v_tp1[i - 2]);
        v_t[i] = std::max(v1, v2) * half;
    }
}

Floating value_iteration() {
    std::array<std::array<Floating, xd>, td> V;
    for (int i = 0; i <= x_mid; i++) {
        V.back()[i] = 0;
    }
    for (int i = x_mid + 1; i < xd; i++) {
        V.back()[i] = 1;
    }

    for (int t = T - 1; t >= 0; t--) {
        value_iterate(V[t + 1], V[t], 2 * t);
    }

    return V[0][x_mid];
}

static constexpr const int SAMPLES = 10000;
__attribute__((optnone)) int main() {
    value_iteration();
    int total = 0;
    for (int i = 0; i < SAMPLES; i++) {
        const auto start = std::chrono::high_resolution_clock::now();
        const auto V = value_iteration();
        const auto end = std::chrono::high_resolution_clock::now();
        total += std::chrono::duration_cast<std::chrono::microseconds>(end
                                                                       - start)
                         .count();
    }
    std::cout << value_iteration() << std::endl;
    std::cout << "Time: " << total / SAMPLES << "us" << std::endl;
}
