import matplotlib.pyplot as plt


def plot(curves: dict, time):
    for c in curves:
        plt.plot(time, curves[c], label=f'{c}')

    plt.legend()
    plt.show()
