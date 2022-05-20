import json
import math
import sys
import plotly.graph_objects as go

import matplotlib.pyplot as plt
import numpy

D = 0.06
H = 0
U_c = 0
L = 12
T = 150.
MINIMAL_T = 0.0001  # approximate minimal T, as it can't be 0, and it should be quite big for fast calculations
EPS = 0.01
EPS_ARRAY = [0.1, 0.01, 0.001, 0.0001, 10 ** -5, 10 ** -6, 10 ** -7]
T_CHECK = 1


def calculate_mu_array_with_length(n: int) -> [float]:
    """
    Calculates roots of equation sin(math.pi * n ) = 0.
    :param n: required number of roots
    :return: roots of equation sin(math.pi * n ) = 0
    """
    # array of roots of sin(math.pi * n ) = 0
    mu_array = [i * math.pi for i in range(1, n)]

    # actually, first element of array should be 0, but as further in program division by 0 occurs, minimal float is
    # inserted
    mu_array.insert(0, sys.float_info.min)

    return mu_array


def u(x: float, t: float, mu_array: [float]) -> float:
    """
    Calculates Fourier sum, also known as v(x, t).
    :param x: x
    :param t: t
    :param mu_array: array of roots of sin(math.pi * n ) = 0
    :return:
    """
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
    """
    Calculates F(n).
    :param n: n
    :param t: t
    :return: F(n)
    """
    return (2 * L ** 2 * math.e ** (-D * math.pi ** 2 * t * n ** 2 / L ** 2)) / (D * math.pi ** 3 * n ** 2 * t)


def estimate_n_min_for_single_t(epsilon: float, t: float) -> int:
    """
    Estimates number of elements in fourier sum for single t
    :param epsilon: precision
    :param t: necessary time
    :return: numer of elements in fourier sum
    """
    i = 1
    while f(i, t) > epsilon:
        i += 1
    return i


def estimate_n_min(epsilon: float, t_array: [float]) -> [int]:
    """
    Estimates number of elements in fourier sum for each t in t_array.
    Also known as N(eps)
    :param epsilon: precision
    :param t_array: array of necessary times
    :return: array of numer of elements in fourier sum accordingly for each t
    """
    n_array = []
    for single_t in t_array:
        n_array.append(estimate_n_min_for_single_t(epsilon, single_t))

    return n_array


def build_plot(x: [float], y_array: [[float]], sections: [float], x_label: [str], y_label: [str], sections_label: [str]) \
        -> plt.Figure:
    """
    Builds plot for given parameters
    :param y_array: y
    :param sections_label:
    :param y_label:
    :param x_label:
    :param x: x
    :param sections: sections
    """
    fig = go.Figure()
    for y, section in zip(y_array, sections):
        fig.add_trace(go.Line(x=x, y=y, mode='lines', name=sections_label + str(section)))

    return fig


def estimate_experimental_n(epsilon: float, x_array: [float], t: float, mu_array: [float], n: int) -> int:
    """
    Experimentally estimates number of elements of Fourier's sum needed to satisfy given precision.
    :param n: estimated with N(eps) n
    :param t: t
    :param epsilon: precision
    :param x_array: x
    :param mu_array: roots of array of roots of sin(math.pi * n ) = 0
    :return: array of numer of elements in fourier sum accordingly for each t
    """
    i = n
    while all([abs(u(x, t, mu_array[i - 1:i])) < epsilon for x in x_array]):
        i -= 1

    return i


def print_fourier_sum_with_all_mu(x: float, t: float, mu_array: [float]):
    """
    Prints Fourier's sum with different number of elements
    :param x: x
    :param t: t
    :param mu_array: roots of array of roots of sin(math.pi * n ) = 0
    :return: None
    """
    for i in range(1, len(mu_array)):
        print(u(x, t, mu_array[:i]))


def print_matrix(matrix):
    """
    Some terrifying method from  https://stackoverflow.com/questions/13214809/pretty-print-2d-list#:~:text=90,a%20bigger%20matrix%3A
    :param matrix: matrix to print
    :return: None
    """
    s = [[str(e) for e in row] for row in matrix]
    lens = [max(map(len, col)) for col in zip(*s)]
    fmt = ' | '.join('{{:{}}}'.format(x) for x in lens)
    table = [fmt.format(*row) for row in s]
    print('\n'.join(table))


def calculate(inputs):
    print(inputs)
    D, L, T = inputs
    # estimate number of elements in fourier's sum
    t_values = [MINIMAL_T, T / 3, 2 * T / 3, T]
    x_values = [0, L/2, 2*L/3, L]
    n_array = estimate_n_min(EPS, t_values)

    print("With given precision: " + str(EPS))
    print_matrix([["T: "] + t_values, ["N: "] + n_array])

    mu_array = calculate_mu_array_with_length(max(n_array))

    x = numpy.linspace(0, L, 500)
    t = numpy.linspace(0, T, 500)

    # check difference between n found by estimate_n_min and experimental one
    print("For t = " + str(T_CHECK))

    eps_array = ["EPS :"] + EPS_ARRAY
    n_min = ["N_min: "]
    n_exp = ["N_exp: "]
    for epsilon in EPS_ARRAY:
        current_n_min = estimate_n_min_for_single_t(epsilon, T_CHECK)
        n_min.append(str(current_n_min))
        n_exp.append(
            str(estimate_experimental_n(epsilon, x, T_CHECK, mu_array, current_n_min)))

    print_matrix([eps_array, n_min, n_exp])

    # for each t, x mu_array is reduced to satisfy given precision
    y_array = []
    for n, _t in zip(n_array, t_values):
        y_array.append([u(_x, _t, mu_array[:n]) for _x in x])

    plot1 = build_plot(x, y_array, t_values, x_label="x", y_label="U(x, t)", sections_label="t = ")

    t_array = []
    for n, _x in zip(n_array, x_values):
        t_array.append([u(_x, _t, mu_array[:n]) for _t in t])

    plot2 = build_plot(t, t_array, x_values, x_label="t", y_label="U(x, t)", sections_label="x = ")
    # plt.show()

    return plot1, plot2


