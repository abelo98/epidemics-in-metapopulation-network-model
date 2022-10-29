import matplotlib.pyplot as plt
from os import listdir
from os.path import join
from .error_functions import mse

from sympy import im
from ..mmodel.params_estimation.estimate_params_test import estimator_test

import numpy as np


def get_data_simulation(est: estimator_test, numba):
    days = np.linspace(0, 300, 300)
    return est.start_sim(days, numba)


def plot(curve_paires: list, time):
    for pair in curve_paires:
        for c in pair:
            if (c.__contains__('empleando')):
                plt.plot(time, pair[c], label=f'{c}', linestyle='--')
            else:
                plt.plot(time, pair[c], label=f'{c}')

        plt.legend()
        plt.show()


def plot_est_and_original():
    network = 'tests/mmodel/simple/simple_network.json'
    params_original = 'tests/mmodel/simple/params/params.json'
    estimations_path = 'tests/mmodel/simple/estimation'

    files = [join(estimations_path, f) for f in listdir(estimations_path)]

    est = estimator_test(network_path=network, params=params_original)
    ydata_original = get_data_simulation(est, False)['I']
    original_plus_ests = []

    for file in files:
        est = estimator_test(network_path=network, params=file)
        label = file.split(sep='.')[0]
        label = label.split(sep='/')[-1]
        y_est = get_data_simulation(est, False)['I']
        original_plus_ests.append({'curva original': ydata_original, 'curva empleando ' +
                                   label: y_est})
        print(
            f'MSE original and {label}: {mse(y_est,ydata_original)}')

    plot(original_plus_ests, np.linspace(0, 300, 300))
