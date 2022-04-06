import math
import matplotlib.pyplot as plt
import numpy

D = 0.06
H = 0
U_c = 0
L = 12
T = 150


def u(x, t, mu_array):
    _sum = 0

    for mu_k in mu_array:
        _sum += \
            1 / mu_k * \
            math.e ** (-D * mu_k ** 2 * t / L ** 2) * \
            math.cos(mu_k * x / L) * \
            math.sin(mu_k / 4) * \
            math.cos(mu_k / 2)

    return 4 * _sum


def mian():
    mu_array = [i * math.pi for i in range(1, 101)]

    x = numpy.linspace(0, L, 500)

    y1 = [u(_x, 0, mu_array) for _x in x]
    y2 = [u(_x, T / 3, mu_array) for _x in x]
    y3 = [u(_x, 2 * T / 3, mu_array) for _x in x]
    y4 = [u(_x, T, mu_array) for _x in x]

    plt.plot(x, y1, label="t = 0")
    plt.plot(x, y2, label="t = T/3")
    plt.plot(x, y3, label="t = 2*T/3")
    plt.plot(x, y4, label="t = T")

    plt.xlabel("x")
    plt.ylabel("U(x, t)")
    plt.legend()

    plt.show()


if __name__ == '__main__':
    mian()
