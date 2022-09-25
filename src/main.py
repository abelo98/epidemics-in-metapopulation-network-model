from mmodel.params_estimation.calc_params import *
from mmodel.data_manager.data_reader import Reader
from mmodel.data_manager.data_cleaner import Cleaner
from mmodel.data_manager.data_operations import data_operator
from mmodel.json_manager.json_processor import *

from mmodel.constants import *


def main():
    est = estimator(days=200)
    data_conf_path = "data_cov/cv19_conf_mun.xlsx"
    data_dead_path = "data_cov/cv19_fall_mun.xlsx"
    paramas_estimated_json = f"tests/mmodel/network_correct_municipality_dist/parameters_estimated_d{START_INFECTED}.json"

    # ydata = initialize()

    df_conf = Reader.get_data(data_conf_path)
    df_dead = Reader.get_data(data_dead_path)

    df_conf_havana = Cleaner.select_rows(df_conf, MUNCPS)
    df_dead_havana = Cleaner.select_rows(df_dead, MUNCPS)

    df_conf_less_dead_havana = data_operator.get_conf_less_dead(
        df_conf_havana, df_dead_havana)

    acc_infected = data_operator.calc_infected(df_conf_less_dead_havana)

    acc_infected_combine = data_operator.combine_infected_all_mcps(
        acc_infected)

    # new_paramas_to_save = est.get_params_estimation(current_paramas_json,
    #                                                 acc_infected, ["beta", "gamma"])

    new_paramas_to_save = est.get_params_estimation_metamodel(
        acc_infected_combine, ["beta", "gamma"])

    save_file_as_json(paramas_estimated_json, new_paramas_to_save)


if __name__ == "__main__":
    main()
