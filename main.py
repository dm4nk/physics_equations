import math
import sys

import matplotlib.pyplot as plt
import numpy

D = 0.06
H = 0
U_c = 0
L = 12
T = 150.
MINIMAL_T = 0.0001  # approximate minimal T, as it can't be 0, and it should be quite big for fast calculations
EPS = 0.000005


def u(x: float, t: float, mu_array) -> float:
    _sum = 0

    for mu_k in mu_array:
        _sum += \
            1 / mu_k * \
            math.e ** (-D * mu_k ** 2 * t / L ** 2) * \
            math.cos(mu_k * x / L) * \
            math.sin(mu_k / 4) * \
            math.cos(mu_k / 2)

    return 4 * _sum


def f(n: int, t: float) -> float:
    return (2 * math.e ** (-D * math.pi ** 2 * t * n ** 2 / L ** 2) * L ** 2) / (math.pi ** 3 * n ** 2 * t)


def estimate_n_for(epsilon: float, t_array: [float]) -> [int]:
    i = 1
    n_array = []
    for single_t in t_array:
        while f(i, single_t) > epsilon:
            i += 1
        n_array.append(i)
        i = 1
    return n_array


def build_plot(x: [float], y_array: [[float]]) -> None:
    plt.plot(x, y_array[0], label="t = 0.0001")
    plt.plot(x, y_array[1], label="t = T/3")
    plt.plot(x, y_array[2], label="t = 2*T/3")
    plt.plot(x, y_array[3], label="t = T")
    plt.xlabel("x")
    plt.ylabel("U(x, t)")
    plt.legend()
    plt.show()


def main():
    # estimate number of elements in fourier's sum
    t_array = [MINIMAL_T, T / 3, 2 * T / 3, T]
    n_array = estimate_n_for(EPS, t_array)
    print("for T - N\n" + " | ".join(str(t) + " - " + str(n) for n, t in zip(n_array, t_array)))

    # array of roots of sin(math.pi * n ) = 0
    mu_array = [i * math.pi for i in range(1, max(n_array))]

    # actually, first element of array should be 0, but as further in program division by 0 occurs, minimal float is
    # inserted
    mu_array.insert(0, sys.float_info.min)

    x = numpy.linspace(0, L, 500)
    y_array = []

    # for each t mu_array is reduced to satisfy given precision
    for n, t in zip(n_array, t_array):
        y_array.append([u(_x, t, mu_array[:n]) for _x in x])

    build_plot(x, y_array)


if __name__ == '__main__':
    main()
