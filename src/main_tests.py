import sys
from mmodel.data_manager.data_operations import data_operator

from mmodel.params_estimation.estimate_params_test import estimator_SEAIR, estimator_test
from mmodel.params_estimation.estimator_class import estimator_SIR
from mmodel.json_manager.json_processor import *
import numpy as np
from mmodel.constants import *

from utils.error_functions import mse
from utils.plotter import *

from datetime import date

import os


def plot_est_and_original(y1, y2, label_y1, label_y2):
    min_len = min(len(y1), len(y2))
    days = np.linspace(0, min_len, min_len)

    print(f'max x {label_y1}: {y1[:min_len].argmax()}')
    print(f'max y {label_y1}: {y1[:min_len].max()}')

    print(f'max x {label_y2}: {y2[:min_len].argmax()}')
    print(f'max y {label_y2}: {y2[:min_len].max()}')

    plot_values(y1[:min_len], y2[:min_len], days, label_y1, label_y2)


def plot_est_and_especial_points(y_est):
    days = np.linspace(0, len(y_est), len(y_est))

    ranges = [(int(y_est.argmax()), int(y_est.argmax())),
              (int(y_est.argmax()), len(y_est)-1)]
    min_maxs = [1, -1]

    points = get_points_in_range(ranges, y_est, min_maxs)
    epidemic_start = date(2020, 3, 20)
    labels_for_points = build_labels_for_especial_points(
        points, epidemic_start)
    sigle_plot_and_itresting_points(days, y_est, points, labels_for_points)


def get_data_simulation(est: estimator_SIR, numba, days, comp):
    return est.start_sim(days, numba)[comp]


def convert_estimation_to_list(set_of_est_values):
    output = []
    for d in set_of_est_values:
        output += list(d.values())
    return np.array(output)


def get_infected_combine(params_est, d_op: data_operator):
    acc_infected = d_op.get_infected_by_muncps(params_est)
    return np.array(d_op.combine_infected_all_mcps(acc_infected))

# def get_death()


def compare_est_with_org(y1, y2):
    min_len = min(len(y1), len(y2))
    print('error:', mse(
        y2[:min_len], y1[:min_len]))


def run_test():
    network = 'tests/mmodel/simple/simple_network.json'
    params_original = 'tests/mmodel/simple/params/params.json'

    methods = ['pso']
    json_names = ['psoNumba']
    #  , 'curve_fitNumba','diff_EvolNumba' , 'pso', 'curve_fit', 'diff_Evol'

    original = np.array([0.25, 0.052, 0.25, 0.052])
    days = np.linspace(0, 300, 300)

    results_path = os.path.join(os.path.abspath(
        os.getcwd()), "correctness_fitting_functions4.txt")

    with open(results_path, "a") as sys.stdout:

        for i, exec in enumerate(json_names):
            m = methods[i % len(methods)]
            apply_numba = exec.__contains__('Numba')
            est = estimator_SEAIR(model_name="model_havana_d29", method=m, iter=6000, network_path=network,
                                  params_path=params_original, numba=apply_numba)
            ydata = get_data_simulation(
                est, numba=apply_numba, days=days, comp="I")
            paramas_estimated_json = f"tests/mmodel/simple/estimation/parameters_estimated_{exec}_d1.json"
            print(" ")
            print(exec)
            print(" ")
            print(m)
            print("*********************************************")
            total_time = 0
            total_mse = 0
            best_mse = np.inf
            iters = 10
            for _ in range(iters):
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
            print(f"mean_time {total_time/iters}")
            print(f"mean_error {total_mse/iters}")
            print("*********************************************")


def main():
    active_path = 'data_cov/cv19_conf_mun.xlsx'
    death_path = 'data_cov/cv19_fall_mun.xlsx'
    # network1 = 'tests/mmodel/network_correct_municipality_dist/habana_network_geographic.json'
    # params_est1 = 'tests/mmodel/network_correct_municipality_dist/estimation/parameters_estimated_PSO_Numba_GPU_d29_iter-50000.json'
    # network2 = 'tests/mmodel/without_centro_habana_all_connections/havana_network_correct_perc.json'
    # params_est2 = 'tests/mmodel/without_centro_habana_all_connections/estimation/parameters_estimated_PSO_Numba_GPU_d29_iter-50000.json'
    # arreglar q numba se pide en est y sim
    # days = np.linspace(0, 1111, 1111)
    # d_op = data_operator(death_path, active_path)

    # est = estimator_test(network_path=network1,
    #                      params=params_est1, numba=False)
    # y_estimated = get_data_simulation(est, False, days, 'I')
    # infected_all_combine = get_infected_combine(params_est2, d_op)

    # est2 = estimator_test(network_path=network2,
    #                       params=params_est2, numba=False)
    # y_estimated2 = get_data_simulation(est2, False, days, 'I')

    # label1 = 'I(t) estimado todos los municipios conectados'
    # label2 = 'I(t) estimado municipios colindantes conectados'
    run_test()
    # compare_est_with_org(y_estimated2, y_estimated)
    # plot_est_and_original(y_estimated2, infected_all_combine, label1, label2)
    # plot_est_and_especial_points(y_estimated)


if __name__ == "__main__":
    main()
