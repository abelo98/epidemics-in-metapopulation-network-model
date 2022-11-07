from mmodel.params_estimation.estimator_class import estimator_SIR
from mmodel.data_manager.data_operations import data_operator
from mmodel.json_manager.json_processor import *
from mmodel.constants import *


def calc_params_with_acc_infected_combine(est: estimator_SIR, acc_infected, d_op):
    return est.get_params_estimation_combine_infected(acc_infected, d_op)


def main():
    iters = 1

    networks = [
        'tests/mmodel/havana_geo_connections/havana_geo_correct_perc.json']

    params = [
        'tests/mmodel/havana_geo_connections/params/parameters_d16.json']

    paramas_estimated_jsons = [
        f"tests/mmodel/havana_geo_connections/estimation/parameters_estimated_PSO_Numba_GPU_d{START_INFECTED}_iter-{iters}.json"]

    data_conf_path = "data_cov/cv19_conf_mun.xlsx"
    data_dead_path = "data_cov/cv19_fall_mun.xlsx"

    for i, n in enumerate(networks):
        est = estimator_SIR(model_name=f"model_havana_d{START_INFECTED}", method='pso', network_path=n,
                            params_path=params[i], iter=iters, numba=True)

        d_op = data_operator(data_dead_path, data_conf_path)

        acc_infected = d_op.get_infected_by_muncps(params[i])

        new_paramas_to_save, time = calc_params_with_acc_infected_combine(
            est, acc_infected, d_op)

        print(f'elapsed time: {time} s')
        save_file_as_json(paramas_estimated_jsons[i], new_paramas_to_save)


if __name__ == "__main__":
    main()
