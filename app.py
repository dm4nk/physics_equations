from model.model import Model
from matplotlib import pyplot as plt
D = 0.06
L = 12
T = 150
EPS = 0.01


def main():
    Model(D, L, T, EPS).calculate()
    plt.show()


if __name__ == "__main__":
    main()
