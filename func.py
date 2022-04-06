import math
from Constants import Constants

p = Constants.H.value * Constants.L.value
L = Constants.L.value
D = Constants.D.value


def func(mu):
    return math.sin(mu)


def psi(x):
    return 0 if x < L / 4 or x > 3 / 4 * L else 1


def u(x, t, mu_array):
    _sum = 0.

    for mu_k in mu_array:
        _sum += \
            2 / mu_k * \
            math.e ** (-D * mu_k ** 2 * t / L ** 2) * \
            math.cos(mu_k * x / L) * \
            (math.sin(3 * mu_k / 4) - math.sin(mu_k / 4))

    return _sum
