import sys
from mmodel.data_manager.data_operations import data_operator

from mmodel.params_estimation.estimate_params_test import estimator_SEAIR, estimator_test
from mmodel.params_estimation.estimator_class import estimator_SIR, estimator_SAIR
from mmodel.params_estimation.classic_models import *
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
    print(f'max y {label_y1}: {int(y1[:min_len].max())}')

    print(f'max x {label_y2}: {y2[:min_len].argmax()}')
    print(f'max y {label_y2}: {int(y2[:min_len].max())}')

    plot_values(y1[:min_len], y2[:min_len], days, label_y1, label_y2)


def get_min_len(curves):
    min_len = np.inf
    for curve in curves:
        if len(curve) < min_len:
            min_len = len(curve)
    return min_len


def plot_multiple(curves, labels):
    min_len = get_min_len(curves)

    days = np.linspace(0, min_len, min_len)

    for i, curve in enumerate(curves):
        x = curve[:min_len].argmax()
        print(f'max x {labels[i]}: {x}')
        print(f'max y {labels[i]}: {int(curve[x])}')

    curves = [c[:min_len] for c in curves]
    plot_values_multiple_curves(curves, days, labels)


def plot_est_and_especial_points(y_est, label):
    days = np.linspace(0, len(y_est), len(y_est))
    # (0, 178), (118, int(y_est.argmax())),
    ranges = [(int(y_est.argmax()), int(y_est.argmax())),
              (int(y_est.argmax()), len(y_est)-1)]
    min_maxs = [1, -1]

    points = get_points_in_range(ranges, y_est, min_maxs)
    epidemic_start = date(2020, 3, 26)
    labels_for_points = build_labels_for_especial_points(
        points, epidemic_start)
    sigle_plot_and_itresting_points(
        days, y_est, label, points, labels_for_points)


def get_data_simulation(est: estimator_SIR, numba, days):
    return est.start_sim(days, numba)


def convert_estimation_to_list(set_of_est_values):
    output = []
    for d in set_of_est_values:
        output += list(d.values())
    return np.array(output)


def get_infected_combine(params_path, d_op: data_operator):
    acc_infected = d_op.get_infected_by_muncps(params_path)
    return np.array(d_op.combine_infected_all_mcps(acc_infected))

# def get_death()


def compare_est_with_org(y1, y2):
    min_len = min(len(y1), len(y2))
    print('error:', mse(
        y2[:min_len], y1[:min_len]))


def run_test():
    network = 'tests/mmodel/simple_sirs/simple_network.json'
    params_original = 'tests/mmodel/simple_sirs/params/simple_params.json'

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

    # ****************CLASSIC*******************
    network1 = 'tests/mmodel/havana_all_Conn_Classic_SIR/simple_network.json'
    params_path1 = 'tests/mmodel/havana_all_Conn_Classic_SIR/estimation/parameters_estimated_pso_SIR_Classic_Numba_GPU_d29_iter-50000.json'

    network2 = 'tests/mmodel/havana_all_Conn_Classic_SAIR/simple_network.json'
    params_path2 = 'tests/mmodel/havana_all_Conn_Classic_SAIR/estimation/parameters_estimated_pso_SIR_Classic_Numba_GPU_d29_iter-50000.json'

    # ****************METAPOP*******************
    network3 = 'tests/mmodel/havana_all_connections/havana_network_correct_perc.json'
    params_path3 = 'tests/mmodel/havana_all_connections/estimation/parameters_estimated_PSO_Numba_GPU_d29_iter-50000.json'

    network4 = 'tests/mmodel/havana_geo_connections/havana_geo_correct_perc.json'
    params_path4 = 'tests/mmodel/havana_geo_connections/estimation/parameters_estimated_PSO_Numba_GPU_d29_iter-50000.json'

    network5 = 'tests/mmodel/without_centro_habana_all_connections/havana_network_correct_perc.json'
    params_path5 = 'tests/mmodel/without_centro_habana_all_connections/estimation/parameters_estimated_PSO_Numba_GPU_d29_iter-50000.json'

    network6 = 'tests/mmodel/without_plaza_all_connections/havana_network_correct_perc.json'
    params_path6 = 'tests/mmodel/without_plaza_all_connections/estimation/parameters_estimated_PSO_Numba_d29_iter-50000.json'

    network7 = 'tests/mmodel/havana_geo_connections_SAIR/havana_geo_correct_perc.json'
    params_path7 = 'tests/mmodel/havana_geo_connections_SAIR/estimation/parameters_estimated_pso_SAIR_Numba_GPU_d29_iter-12000.json'

    # arreglar q numba se pide en est y sim
    days = np.linspace(0, 5000, 5000)
    d_op = data_operator(death_path, active_path)
    infected_all_combine = get_infected_combine(params_path3, d_op)

    est1 = estimator_SIR_classic(network_path=network1,
                                 params_path=params_path1, numba=False)
    y_estimated = get_data_simulation(est1, False, days)
    y_infected1 = y_estimated['I']

    est2 = estimator_SAIR_classic(network_path=network2,
                                  params_path=params_path2, numba=False)
    y_estimated = get_data_simulation(est2, False, days)
    y_infected2 = y_estimated['I']
    y_asyntomatic2 = y_estimated['A']

    est_hav_allConn = estimator_SIR(network_path=network3,
                                    params_path=params_path3, numba=False)
    y_estimated_hav_allConn = get_data_simulation(est_hav_allConn, False, days)
    y_infected_hav_allConn = y_estimated_hav_allConn['I']

    # est_hav_geoConn = estimator_SIR(network_path=network4,
    #                                 params_path=params_path4, numba=False)
    # y_estimated_hav_geoConn = get_data_simulation(est_hav_geoConn, False, days)
    # y_infected_hav_geoConn = y_estimated_hav_geoConn['I']

    # est_centroHav = estimator_SIR(network_path=network5,
    #                               params_path=params_path5, numba=False)
    # y_estimated_centroHav = get_data_simulation(est_centroHav, False, days)
    # y_infected_centroHav = y_estimated_centroHav['I']

    # est_plaza = estimator_SIR(network_path=network6,
    #                           params_path=params_path6, numba=False)
    # y_estimated_plaza = get_data_simulation(est_plaza, False, days)
    # y_infected_plaza = y_estimated_plaza['I']

    # est_hav_geo_SAIR = estimator_SAIR(network_path=network7,
    #                                   params_path=params_path7, numba=False)
    # y_estimated_hav_geoConn_SAIR = get_data_simulation(
    #     est_hav_geo_SAIR, False, days)
    # y_infected_hav_geoConn_SAIR_I = y_estimated_hav_geoConn_SAIR['I']
    # y_infected_hav_geoConn_SAIR_A = y_estimated_hav_geoConn_SAIR['A']

    label1 = 'I(t) SIR clasico Habana todos los municipios conectados'
    label2 = 'I(t) SAIR clasico Habana todos los municipios conectados'
    label3 = 'A(t) SAIR clasico Habana todos los municipios conectados'
    # label4 = 'I(t) SIR metapoblaciones todos los municipios conectados'
    label4 = 'I(t) SIR (metapoblaciones), estimado Habana con todos los municipios conectados '
    label5 = 'I(t) SIR (metapoblaciones), estimado Habana con municipios colindantes conectados'
    label6 = 'I(t) estimado sin Centro Habana'
    label7 = 'I(t) estimado sin Plaza'
    label8 = 'I(t) SAIR (metapoblaciones), estimado Habana municipios colindantes conectados'
    label9 = 'A(t) SAIR (metapoblaciones), estimado Habana municipios colindantes conectados'

    label10 = 'datos reales'

    # # run_test()
    # compare_est_with_org(y_infected2,
    #                      infected_all_combine[14:])

    plot_multiple([y_infected_hav_allConn, y_infected1, y_infected2, infected_all_combine],
                  [label4, label1, label2, label10])
    plot_multiple([y_infected_hav_allConn, y_infected1, y_infected2, y_asyntomatic2],
                  [label4, label1, label2, label3])

    # plot_multiple([y_infected2, y_asyntomatic2],
    #               [label2, label3])

    # plot_est_and_original(y_infected1, y_infected_hav_allConn, label1, label4)
    # plot_est_and_especial_points(
    #     y_infected2, 'estimado I(t)')
    # plot_est_and_especial_points(
    #     y_asyntomatic2, 'estimado A(t)')


if __name__ == "__main__":
    main()
