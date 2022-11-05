import numpy as np
from mmodel.params_estimation.estimate_params_test import estimator_test
import matplotlib.pyplot as plt
from os import listdir
from os.path import join
from .error_functions import mse
import datetime


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


def plot_network_est_and_original():
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


def plot_values(data_org, data_est, time, label_y1, label_y2):
    plt.plot(time, data_org,
             label=label_y1, linestyle='--')
    plt.plot(time, data_est, label=label_y2)
    plt.xlabel("tiempo en días")
    plt.ylabel("activos por día")
    plt.legend()
    plt.show()


def sigle_plot_and_itresting_points(x, y, points: list, dates: list):
    plt.plot(x, y, label='I(t) estimado')
    for i, point in enumerate(points):
        p_x = point[0]
        p_y = point[1]
        plt.plot(p_x, p_y, marker="o", color="green",
                 label=f'p{i}: {dates[i]}')
        if i != 1:
            plt.annotate(f'p{i}{(point[0], int(point[1]))}',
                         (point[0], point[1]),
                         textcoords="offset points",
                         xytext=(0, 3),
                         ha='center')
        else:
            plt.annotate(f'p{i}{(point[0], int(point[1]))}',
                         (point[0], point[1]),
                         textcoords="offset points",
                         xytext=(33, -8),
                         ha='center')
    plt.xlabel("tiempo en días")
    plt.ylabel("activos por día")
    plt.legend()
    plt.show()


def get_points_in_range(ranges: list, data, min_maxs: list):
    points = []
    for i, min_max in enumerate(min_maxs):
        if min_max == -1:
            best = np.inf
        else:
            best = -np.inf

        start = ranges[i][0]
        end = ranges[i][1]
        day = 0
        while start <= end:
            if min_max == -1 and data[start] < best:
                best = data[start]
                day = start
            elif min_max == 1 and data[start] > best:
                best = data[start]
                day = start
            start += 1
        points.append((day, best))
    return points


def build_labels_for_especial_points(points: list, start_date: datetime.date):
    return [start_date + datetime.timedelta(days=p[0]) for p in points]
