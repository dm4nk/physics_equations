from math import ceil

import numpy as np


def build_slices(v, arr, values, label):
    h = arr[1] - arr[0]
    print(h)
    result = []
    for value in values:
        k = ceil(value / h)
        if label == 'x':
            result.append(v[:, k])
        else:
            result.append(v[k, :])
    return result


class NewModel:
    def __init__(self, D=0.06, L=12, T=150, EPS=100, x=[], t=[], x_values=[], t_values=[]):
        self.__D = D
        self.__L = L
        self.__T = T
        self.__EPS = EPS
        self.__x = x
        self.__t = t
        self.__x_values = x_values
        self.__t_values = t_values

    def set_parameters(self, D=0.06, L=12, T=150, EPS=100, x=[], t=[], x_values=[], t_values=[]):
        self.__D = D
        self.__L = L
        self.__T = T
        self.__EPS = EPS
        self.__x = x
        self.__t = t
        self.__x_values = x_values
        self.__t_values = t_values

    def psi(self, x) -> float:
        return 1 if self.__L / 4 < x < 3 * self.__L / 4 else 0

    def implicit_solution(self, x: [float], t: [float], D: float, ) -> [[float]]:
        I, K = len(x) - 1, len(t) - 1
        hx = x[1] - x[0]
        ht = t[1] - t[0]

        gamma = D * ht / (hx ** 2)

        p, q, u = np.full(I, -10.), np.full(I, -10.), np.full((K + 1, I + 1), -10.)

        for i in range(0, I + 1):
            u[0][i] = self.psi(x[i])

        p[0] = 2 * gamma / (1 + 2 * gamma)
        for i in range(1, I):
            p[i] = gamma / (1 + (2 - p[i - 1]) * gamma)

        for k in range(1, K + 1):

            q = np.full(I, -10.)
            q[0] = u[k - 1][0] / (1 + 2 * gamma)
            for i in range(1, I):
                q[i] = (u[k - 1][i] + gamma * q[i - 1]) / (1 + (2 - p[i - 1]) * gamma)

            numerator = u[k - 1][I - 1] + 2 * gamma * q[I - 2]
            divider = 1 + 2 * gamma * (1 - p[I - 2])
            u[k][I - 1] = numerator / divider
            u[k][I] = u[k][I - 1] + 1 / 2 / gamma * (u[k][I - 1] - u[k - 1][I - 1])

            for i in range(I - 2, -1, -1):
                u[k][i] = p[i] * u[k][i + 1] + q[i]

        return u

    def build_plot(self):
        v = self.implicit_solution(self.__x, self.__t, self.__D)

        # plot1 = build_plot(x, build_slices(v, t, t_values, 'x'), t_values, x_label="x", sections_label="t = ")
        # plot2 = build_plot(t, build_slices(v, t, x_values, 't'), x_values, x_label="t", sections_label="x = ")

        return build_slices(v, self.__x, self.__x_values, 't'), build_slices(v, self.__t, self.__t_values, 'x')

    def set_end_bild(self, D, L, T, EPS, X, Y, X_VALS, T_VALS):
        self.set_parameters(D, L, T, EPS, X, Y, X_VALS, T_VALS)
        return self.build_plot()
