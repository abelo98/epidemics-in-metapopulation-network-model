import sys
from mmodel.data_manager.data_operations import data_operator

from mmodel.params_estimation.estimate_params_test import estimator_test
from mmodel.json_manager.json_processor import *
import numpy as np
from mmodel.constants import *

from utils.error_functions import mse, get_error
from utils.plotter import plot_values

import os


def plot_est_and_original(network, active_path, death_path, params_est):
    d_op = data_operator()
    est = estimator_test(network_path=network, params=params_est)

    acc_infected = d_op.get_infected_by_muncps(active_path, death_path)
    acc_infected_combine = d_op.combine_infected_all_mcps(acc_infected)
    days = np.linspace(0, len(acc_infected_combine), len(acc_infected_combine))
    y_est = est.start_sim(days, False)['I']
    print(f'day with the most infected people: {y_est.argmax()}')
    print(f'most infected people reported: {y_est.max()}')

    plot_values(acc_infected_combine, y_est, days)


def get_data_simulation(est: estimator_test, numba):
    days = np.linspace(0, 300, 300)
    return est.start_sim(days, numba)


def convert_estimation_to_list(set_of_est_values):
    output = []
    for d in set_of_est_values:
        output += list(d.values())
    return np.array(output)


def compare_est_with_org(network, active_path, death_path, params_est):
    d_op = data_operator()

    acc_infected = d_op.get_infected_by_muncps(
        active_path, death_path, params_est)
    acc_infected_combine = d_op.combine_infected_all_mcps(acc_infected)

    print('error:', get_error(network, params_est, acc_infected_combine))


def run_test():
    network = 'tests/mmodel/simple/simple_network.json'
    params_original = 'tests/mmodel/simple/params/params.json'

    methods = ['pso', 'curve_fit', 'diff_evol']
    json_names = ['psoNumba', 'curve_fitNumba',
                  'diff_EvolNumba']
    #   , 'pso', 'curve_fit', 'diff_Evol'

    original = np.array([0.25, 0.052, 0.25, 0.052])

    results_path = os.path.join(os.path.abspath(
        os.getcwd()), "correctness_fitting_functions3.txt")

    with open(results_path, "a") as sys.stdout:

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
                current_mse = mse(estimated_params, original)

                total_mse += current_mse

                if current_mse < best_mse:
                    best_mse = current_mse
                    save_file_as_json(paramas_estimated_json, built_json)

            print(" ")
            print(f"mean_time {total_time/30}")
            print(f"mean_error {total_mse/30}")
            print("*********************************************")


def main():
    network = 'tests/mmodel/havana_all_connections/havana_network_correct_perc.json'
    active_path = 'data_cov/cv19_conf_mun.xlsx'
    death_path = 'data_cov/cv19_fall_mun.xlsx'
    params_est = 'tests/mmodel/havana_all_connections/estimation/parameters_estimated_Levenberg-Marquardt_Numba_GPU_d29_iter-1000000.json'
    run_test()
    # compare_est_with_org(network, active_path, death_path, params_est)
    # plot_est_and_original(network, active_path, death_path, params_est)


if __name__ == "__main__":
    main()
