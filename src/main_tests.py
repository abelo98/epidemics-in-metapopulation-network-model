from mmodel.params_estimation.estimator_class import estimator
# from mmodel.params_estimation.calc_params_lmfit import *
from mmodel.data_manager.data_reader import Reader
from mmodel.data_manager.data_cleaner import Cleaner
from mmodel.data_manager.data_operations import data_operator
from mmodel.json_manager.json_processor import *
import numpy as np
from mmodel.constants import *


def get_data_simulation(est: estimator):
    days = np.linspace(0, 300, 300)
    return est.start_sim(days)


def main():
    est = estimator(
        "src/mmodel/params_estimation/params_guess.json", method='pso')

    paramas_estimated_json = f"tests/mmodel/havana_full_network/estimation/parameters_estimated_d{START_INFECTED}.json"

    ydata = get_data_simulation(est)['I']

    new_paramas_to_save = est.get_params_estimation_combine_infected(ydata)

    save_file_as_json(paramas_estimated_json, new_paramas_to_save)


if __name__ == "__main__":
    main()
