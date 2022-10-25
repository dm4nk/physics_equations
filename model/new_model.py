from math import ceil

import numpy as np


def build_slices(u, arr, values, label):
    h = arr[1] - arr[0]
    result = []
    for value in values:
        k = ceil(value / h)
        if label == 't':
            result.append(u[:, k])
        else:
            result.append(u[k, :])
    return result


class NewModel:
    def __init__(self, C=2.64, R=3, T=80, K=0.13, A=0.002, L=0.5, x=[], t=[], x_values=[], t_values=[]):
        self.__C = C
        self.__R = R
        self.__T = T
        self.__K = K
        self.__A = A
        self.__L = L

        self.__r = x
        self.__t = t

        self.__x_values = x_values
        self.__t_values = t_values

    def set_parameters(self, C=2.64, R=3, T=80, K=0.13, A=0.002, L=0.5, x=[], t=[], x_values=[], t_values=[]):
        self.__C = C
        self.__R = R
        self.__T = T
        self.__K = K
        self.__A = A
        self.__L = L

        self.__r = x
        self.__t = t

        self.__x_values = x_values
        self.__t_values = t_values

    def psi(self, ri) -> float:
        if 0.0 <= ri <= 3.0 / 5.0:
            return 180.0
        else:
            return 0.0

    def implicit_solution(self, r: [float], t: [float], c: float, k: float, a: float, l: float) -> [[float]]:
        I, K = len(r) - 1, len(t) - 1
        hr = r[1] - r[0]
        ht = t[1] - t[0]
        gamma = k * ht / (c * hr ** 2)
        betta = 2.0 * a * ht / (l * c)
        alpha_0 = 1.0 + 4.0 * gamma + betta
        alpha = 1.0 + 2.0 * gamma + betta

        u = np.zeros((K + 1, I + 1))

        for i in range(0, I):
            u[0][i] = self.psi(r[i])

        p_0 = 4.0 * gamma / alpha_0
        q_0 = 1.0 / alpha_0

        for k in range(1, K + 1):
            p, q = np.zeros(I - 1), np.zeros(I - 1)
            p[0] = p_0
            q[0] = q_0 * u[k - 1][0]

            for i in range(1, I - 1):
                e = 1.0 - hr / r[i]
                d = alpha - gamma * hr / r[i] - gamma * p[i - 1] * e
                p[i] = gamma / d
                q[i] = (u[k - 1][i] + gamma * q[i - 1] * e) / d

            e = 1.0 - hr / r[I - 1]
            d = alpha - gamma * hr / r[I - 1] - gamma * p[I - 2] * e
            u[k][I - 1] = (u[k - 1][I - 1] + gamma * q[I - 2] * e) / d

            for i in range(I - 2, -1, -1):
                u[k][i] = p[i] * u[k][i + 1] + q[i]

        return u

    def build_plot(self):
        v = self.implicit_solution(r=self.__r, t=self.__t, c=self.__C, k=self.__K, a=self.__A, l=self.__L)
        return build_slices(v, self.__t, self.__t_values, 'x'), build_slices(v, self.__r, self.__x_values, 't')

    def set_end_bild(self, C, R, T, K, A, L, X, Y, X_VALS, T_VALS):
        self.set_parameters(C=C, R=R, T=T, K=K, A=A, L=L, x=X, t=Y, x_values=X_VALS, t_values=T_VALS)
        return self.build_plot()
