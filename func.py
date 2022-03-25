import math
from scipy.integrate import quad
from Constants import Constants

p = Constants.H.value / Constants.L.value
l = Constants.L.value
D = Constants.D.value
U_c = Constants.U_c.value


def func(mu):
    return math.tan(mu) - p / mu


def psi(x):
    return 0 if x < l/4 or x > 3/4*l else 1


def u(x, t, mu_array):
    _sum = 0.

    for mu_k in mu_array:
        _sum += \
            (mu_k ** 2 + p ** 2) / \
            (p * (p - 1) + mu_k ** 2) * \
            math.e ** (-D * mu_k ** 2 * t / l ** 2) * \
            math.sin(mu_k * x / l) * \
            quad(lambda _x: psi(_x)*math.sin(mu_k * _x / l), 0, l)[0]

    return 2 / l * _sum + U_c
