from math import pi, sin, cos, e

from utils import build_plot

H = 0
U_c = 0
T_CHECK = 1


class OldModel:
    def __init__(self, D=0.06, L=12, T=150, EPS=0.01, x=[], t=[], x_values=[], t_values=[]):
        self.__D = D
        self.__L = L
        self.__T = T
        self.__EPS = EPS
        self.__x = x
        self.__t = t
        self.__x_values = x_values
        self.__t_values = t_values

    def set_params(self, D, L, T, EPS, x, t, x_values, t_values):
        self.__D = D
        self.__L = L
        self.__T = T
        self.__EPS = EPS
        self.__x = x
        self.__t = t
        self.__x_values = x_values
        self.__t_values = t_values

    def u(self, x: float, t: float, n: int) -> float:
        """
        Calculates Fourier sum, also known as v(x, t).
        :param n:
        :param x: x
        :param t: t
        :return:
        """
        _sum = 0
        for k in range(1, n + 1):
            _sum += \
                1 / (pi * k) * \
                e ** (-self.__D * (pi * k) ** 2 * t / self.__L ** 2) * \
                cos(pi * k * x / self.__L) * \
                sin(pi * k / 4) * \
                cos(pi * k / 2)
        return 4 * _sum + 1 / 2

    def f(self, n: int, t: float) -> float:
        """
        Calculates F(n).
        :param n: n
        :param t: t
        :return: F(n)
        """
        return (2 * self.__L ** 2 * e ** (-self.__D * pi ** 2 * t * n ** 2 / self.__L ** 2)) / (
                self.__D * pi ** 3 * n ** 2 * t)

    def estimate_n_min_for_single_t(self, epsilon: float, t: float) -> int:
        """
        Estimates number of elements in fourier sum for single t
        :param epsilon: precision
        :param t: necessary time
        :return: numer of elements in fourier sum
        """
        i = 1
        while self.f(i, t) > epsilon:
            i += 1
        return i

    def estimate_n_min(self, epsilon: float, t_array: [float]) -> [int]:
        """
        Estimates number of elements in fourier sum for each t in t_array.
        Also known as N(eps)
        :param epsilon: precision
        :param t_array: array of necessary times
        :return: array of numer of elements in fourier sum accordingly for each t
        """
        n_array = []
        for single_t in t_array:
            n_array.append(self.estimate_n_min_for_single_t(epsilon, single_t))

        return n_array

    def estimate_experimental_n(self, epsilon: float, x_array: [float], t: float, n: int) -> int:
        """
        Experimentally estimates number of elements of Fourier's sum needed to satisfy given precision.
        :param n: estimated with N(eps) n
        :param t: t
        :param epsilon: precision
        :param x_array: x
        :return: array of numer of elements in fourier sum accordingly for each t
        """
        i = n
        while all([abs(self.u(x, t, i) - self.u(x, t, i - 1)) < epsilon for x in x_array]):
            i -= 1

        return i

    def build_plots(self):
        # estimate number of elements in fourier's sum
        n_array = [int(self.__EPS)] * len(self.__t_values) if self.__EPS.is_integer() \
            else self.estimate_n_min(self.__EPS, self.__t_values)

        print("With given precision: " + str(self.__EPS))

        y_array = []
        for n1, _t1 in zip(n_array, self.__t_values):
            y_array.append([self.u(_x1, _t1, n1) for _x1 in self.__x])

        # plot1 = build_plot(self.__x, y_array, self.__t_values, x_label="x", sections_label="t = ")

        t_array = []
        for _x2 in self.__x_values:
            t_array.append([self.u(_x2, _t2, 100) for _t2 in self.__t])

        # plot2 = build_plot(self.__t, t_array, self.__x_values, x_label="t", sections_label="x = ")

        return y_array, t_array, self.__t_values[1:], n_array

    def set_end_bild(self, D, L, T, EPS, X, Y, X_VALS, T_VALS):
        self.set_params(D, L, T, EPS, X, Y, X_VALS, T_VALS)
        return self.build_plots()
