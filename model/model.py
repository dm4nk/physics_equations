from math import pi, sin, cos, e

import matplotlib.pyplot as plt
import numpy
import plotly.graph_objects as go

H = 0
U_c = 0
MINIMAL_T = 0.0001  # approximate minimal T, as it can't be 0, and it should be quite big for fast calculations
EPS_ARRAY = [0.1, 0.01, 0.001, 0.0001, 10 ** -5, 10 ** -6, 10 ** -7]
T_CHECK = 1


def build_plot(x: [float], y_array: [[float]], sections: [float], x_label: [str], y_label: [str],
               sections_label: [str]) \
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
    fig.update_layout(
        xaxis=dict(
            showgrid=False,
            showticklabels=True,
            linecolor='rgb(204, 204, 204)',
            linewidth=2,
            ticks='outside'
        ),
        yaxis=dict(
            showgrid=False,
            zeroline=False,
            showticklabels=True,
            linecolor='rgb(204, 204, 204)',
            linewidth=2,
            ticks='outside'
        ),
        autosize=True,
        margin=dict(
            autoexpand=True,
            l=100,
            r=100,
            t=110,
        ),
        showlegend=True,
        plot_bgcolor='white'
    )
    fig.update_layout(xaxis_title=x_label, yaxis_title=y_label)
    for y, section in zip(y_array, sections):
        fig.add_trace(go.Line(x=x, y=y, mode='lines', name=sections_label + str(section)))

    return fig


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


class Model:

    def __init__(self, D, L, T, EPS):
        self.__D = D
        self.__L = L
        self.__T = T
        self.__EPS = EPS

    def set_params(self, D, L, T, EPS):
        self.__D = D
        self.__L = L
        self.__T = T
        self.__EPS = EPS

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
        return 4 * _sum + 1/2

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
        while all([abs(self.u(x, t, i) - self.u(x, t, i-1)) < epsilon for x in x_array]):
            i -= 1

        return i

    def calculate(self):
        # estimate number of elements in fourier's sum
        t_values = [MINIMAL_T, self.__T / 3, 2 * self.__T / 3, self.__T]
        x_values = [0, self.__L / 2, 2 * self.__L / 3, self.__L]
        n_array = self.estimate_n_min(self.__EPS, t_values)

        print("With given precision: " + str(self.__EPS))
        print_matrix([["T: "] + t_values, ["N: "] + n_array])

        x = numpy.linspace(0, self.__L, 500)
        t = numpy.linspace(0, self.__T, 500)

        # check difference between n found by estimate_n_min and experimental one
        print("For t = " + str(T_CHECK))

        eps_array = ["EPS :"] + EPS_ARRAY
        n_min = ["N_min: "]
        n_exp = ["N_exp: "]
        for epsilon in EPS_ARRAY:
            current_n_min = self.estimate_n_min_for_single_t(epsilon, T_CHECK)
            n_min.append(str(current_n_min))
            n_exp.append(
                str(self.estimate_experimental_n(epsilon, x, T_CHECK, current_n_min)))

        print_matrix([eps_array, n_min, n_exp])

        # for each t, x number of elements is reduced to satisfy given precision
        y_array = []
        for n1, _t1 in zip(n_array, t_values):
            y_array.append([self.u(_x1, _t1, n1) for _x1 in x])

        plot1 = build_plot(x, y_array, t_values, x_label="x", y_label="U(x, t)", sections_label="t = ")

        t_array = []
        for _x2 in x_values:
            t_array.append([self.u(_x2, _t2, 100) for _t2 in t])

        plot2 = build_plot(t, t_array, x_values, x_label="t", y_label="U(x, t)", sections_label="x = ")

        return plot1, plot2
