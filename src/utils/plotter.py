import matplotlib.pyplot as plt


def plot(curve_paires: list, time):
    for pair in curve_paires:
        for c in pair:
            plt.plot(time, pair[c], label=f'{c}')

        plt.legend()
        plt.show()
