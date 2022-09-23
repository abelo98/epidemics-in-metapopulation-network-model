from mmodel.params_estimation.calc_params import *
from mmodel.data_manager.data_reader import Reader
from mmodel.data_manager.data_cleaner import Cleaner
from mmodel.data_manager.data_operations import data_operator
from mmodel.json_manager.json_processor import *

from mmodel.constants import *


def main():
    # initialize(days=200)
    data_conf_path = "data_cov/cv19_conf_mun.xlsx"
    data_dead_path = "data_cov/cv19_fall_mun.xlsx"
    current_paramas_json = "tests/mmodel/network_correct_municipality_dist/parameters_d16.json"
    paramas_estimated_json = "tests/mmodel/network_correct_municipality_dist/parameters_estimated_d16.json"

    # ydata = initialize()

    df_conf = Reader.get_data(data_conf_path)
    df_dead = Reader.get_data(data_dead_path)

    df_conf_havana = Cleaner.select_rows(df_conf, MUNCPS)
    df_dead_havana = Cleaner.select_rows(df_dead, MUNCPS)

    df_conf_less_dead_havana = data_operator.get_conf_less_dead(
        df_conf_havana, df_dead_havana)

    acc_infected = data_operator.calc_infected(df_conf_less_dead_havana)

    new_paramas_to_save = get_params_estimation(current_paramas_json,
                                                acc_infected, ["beta", "gamma"])

    save_file_as_json(paramas_estimated_json, new_paramas_to_save)


if __name__ == "__main__":
    main()
