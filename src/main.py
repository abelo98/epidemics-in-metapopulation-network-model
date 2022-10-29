from mmodel.params_estimation.estimator_class import estimator
from mmodel.data_manager.data_reader import Reader
from mmodel.data_manager.data_cleaner import Cleaner
from mmodel.data_manager.data_operations import data_operator
from mmodel.json_manager.json_processor import *
import numpy as np
from mmodel.constants import *


def calc_params_with_acc_infected_combine(est: estimator, acc_infected):
    return est.get_params_estimation_combine_infected(acc_infected)


def calc_params_with_acc_infected_by_muncps(est: estimator, acc_infected):
    return est.get_params_estimation_metamodel(acc_infected)


def calc_params_by_munc_model(est: estimator, acc_infected):
    return est.get_params_estimation(acc_infected)


def main():
    iters = 200000
    est = estimator(method='curve_fit', iter=iters, numba=True)
    data_conf_path = "data_cov/cv19_conf_mun.xlsx"
    data_dead_path = "data_cov/cv19_fall_mun.xlsx"
    paramas_estimated_json = f"tests/mmodel/havana_full_network/estimation/parameters_estimated_Levenberg-Marquardt_Numba_d{START_INFECTED}_iter-{iters}.json"

    df_conf = Reader.get_data(data_conf_path)
    df_dead = Reader.get_data(data_dead_path)

    df_conf_havana = Cleaner.select_rows(df_conf, MUNCPS)
    df_dead_havana = Cleaner.select_rows(df_dead, MUNCPS)

    df_conf_less_dead_havana = data_operator.get_conf_less_dead(
        df_conf_havana, df_dead_havana)

    acc_infected = data_operator.calc_infected(df_conf_less_dead_havana)

    new_paramas_to_save, time = calc_params_with_acc_infected_combine(
        est, acc_infected)

    print(f'elapsed time: {time} s')
    save_file_as_json(paramas_estimated_json, new_paramas_to_save)


if __name__ == "__main__":
    main()
