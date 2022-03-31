import math
from scipy.integrate import quad
from Constants import Constants

p = Constants.H.value * Constants.L.value
L = Constants.L.value
D = Constants.D.value
U_c = Constants.U_c.value


def func(mu: float) -> float:
    return math.sin(mu)


def psi(x: float) -> float:
    return 0 if x < L / 4 or x > 3 / 4 * L else 1


def u(x: float, t: float, mu_array: []) -> float:
    _sum = 0.

    for mu_k in mu_array:
        _sum += \
            (mu_k ** 2 + p ** 2) / \
            (p * (p + 1) + mu_k ** 2) * \
            math.e ** (-D * mu_k ** 2 * t / L ** 2) * \
            math.cos(mu_k * x / L) * \
            quad(lambda _x: psi(_x) * math.cos(mu_k * _x / L), 0, L)[0]

    return 2 / L * _sum + U_c
