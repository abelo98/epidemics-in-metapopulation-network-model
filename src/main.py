from mmodel.params_estimation.estimator_class import estimator
from mmodel.data_manager.data_operations import data_operator
from mmodel.json_manager.json_processor import *
from mmodel.constants import *


def calc_params_with_acc_infected_combine(est: estimator, acc_infected):
    return est.get_params_estimation_combine_infected(acc_infected)


def calc_params_with_acc_infected_by_muncps(est: estimator, acc_infected):
    return est.get_params_estimation_metamodel(acc_infected)


def calc_params_by_munc_model(est: estimator, acc_infected):
    return est.get_params_estimation(acc_infected)


def main():
    iters = 50000

    networks = ['tests/mmodel/havana_all_connections/havana_network_correct_perc.json',
                'tests/mmodel/without_centro_habana_all_connections/havana_network_correct_perc.json',
                'tests/mmodel/network_correct_municipality_dist/habana_network_geographic.json']

    params = ['tests/mmodel/havana_all_connections/params/parameters_d16.json',
              'tests/mmodel/without_centro_habana_all_connections/params/parameters_d16.json',
              'tests/mmodel/network_correct_municipality_dist/parameters_estimated_d16.json']

    paramas_estimated_jsons = [f"tests/mmodel/havana_all_connections/estimation/parameters_estimated_PSO_Numba_GPU_d{START_INFECTED}_iter-{iters}.json",
                               f"tests/mmodel/without_centro_habana_all_connections/estimation/parameters_estimated_PSO_Numba_GPU_d{START_INFECTED}_iter-{iters}.json",
                               f"tests/mmodel/network_correct_municipality_dist/estimation/parameters_estimated_PSO_Numba_GPU_d{START_INFECTED}_iter-{iters}.json"]

    for i, n in enumerate(networks):
        est = estimator(method='pso', network_path=n,
                        params=params[i], iter=iters, numba=True)
        d_op = data_operator()

        data_conf_path = "data_cov/cv19_conf_mun.xlsx"
        data_dead_path = "data_cov/cv19_fall_mun.xlsx"

        acc_infected = d_op.get_infected_by_muncps(
            data_conf_path, data_dead_path, params[i])

        new_paramas_to_save, time = calc_params_with_acc_infected_combine(
            est, acc_infected)

        print(f'elapsed time: {time} s')
        save_file_as_json(paramas_estimated_jsons[i], new_paramas_to_save)


if __name__ == "__main__":
    main()
