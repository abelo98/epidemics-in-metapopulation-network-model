import sys
from mmodel.params_estimation.estimate_params_test import estimator_test
from mmodel.json_manager.json_processor import *
import numpy as np
from mmodel.constants import *

from utils.plotter import plot

from os import listdir
from os.path import join


def get_data_simulation(est: estimator_test, numba):
    days = np.linspace(0, 300, 300)
    return est.start_sim(days, numba)


def mse_for_params(params_est, real_params):
    mse = sum((params_est - real_params)**2)/len(real_params)
    return mse


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
            f'MSE original and {label}: {mse_for_params(y_est,ydata_original)}')

    plot(original_plus_ests, np.linspace(0, 300, 300))


def convert_estimation_to_list(set_of_est_values):
    output = []
    for d in set_of_est_values:
        output += list(d.values())
    return np.array(output)


def run_test():
    network = 'tests/mmodel/simple/simple_network.json'
    params_original = 'tests/mmodel/simple/params/params.json'

    methods = ['pso', 'curve_fit', 'diff_evol']
    json_names = ['psoNumba', 'curve_fitNumba',
                  'diff_EvolNumba', 'pso', 'curve_fit', 'diff_Evol']

    original = np.array([0.25, 0.052, 0.25, 0.052])

    with open("/media/abel/TERA/School/5to/Tesis/My work/correctness_fitting_functions.txt", "a") as sys.stdout:

        for i, exec in enumerate(json_names):
            m = methods[i % len(methods)]
            apply_numba = exec.__contains__('Numba')
            est = estimator_test(method=m, iter=6000, network_path=network,
                                 params=params_original, numba=apply_numba)
            ydata = get_data_simulation(est, numba=apply_numba)['I']
            paramas_estimated_json = f"tests/mmodel/simple/estimation/parameters_estimated_{exec}_d1.json"
            print(" ")
            print(exec)
            print(" ")
            print(m)
            print("*********************************************")
            total_time = 0
            total_mse = 0
            best_mse = np.inf
            for _ in range(30):
                current_mse = 0
                built_json, estimated_params, crono = est.get_params_estimation_combine_infected(
                    ydata)
                total_time += crono
                estimated_params = convert_estimation_to_list(estimated_params)
                current_mse = mse_for_params(
                    estimated_params, original)

                total_mse += current_mse

                if current_mse < best_mse:
                    best_mse = current_mse
                    save_file_as_json(paramas_estimated_json, built_json)

            print(" ")
            print(f"mean_time {total_time/30}")
            print(f"mean_error {total_mse/30}")
            print("*********************************************")


def main():
    plot_est_and_original()
    # run_test()


if __name__ == "__main__":
    main()
