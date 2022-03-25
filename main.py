import matplotlib.pyplot as plt
import numpy

from Constants import Constants
from RootFinder import RootFinder
from func import func, u

T = Constants.D.value

if __name__ == '__main__':
    r = RootFinder(0, 313, 0.001)
    mu_array = r.find(func)

    x = numpy.linspace(150, 12, 100)

    y1 = [u(_x, 0, mu_array) for _x in x]
    y2 = [u(_x, T / 3, mu_array) for _x in x]
    y3 = [u(_x, 2 * T / 3, mu_array) for _x in x]
    y4 = [u(_x, T, mu_array) for _x in x]

    plt.plot(x, y1, label="t = 0")
    plt.plot(x, y2, label="t = T/3")
    plt.plot(x, y3, label="t = 2*T/3")
    plt.plot(x, y4, label="t = T")

    plt.xlabel("t")
    plt.ylabel("U(mu, t)")

    plt.legend()

    plt.show()
