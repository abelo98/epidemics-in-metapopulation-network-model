from mmodel.params_estimation.estimate_params_test import estimator_test
from mmodel.json_manager.json_processor import *
import numpy as np
from mmodel.constants import *


def get_data_simulation(est: estimator_test):
    days = np.linspace(0, 300, 300)
    return est.start_sim(days)


def mse_for_params(params_est, real_params):
    return print(sum((params_est - real_params)**2)/len(real_params))


def main():
    est = estimator_test()

    paramas_estimated_json = f"tests/mmodel/simple/estimation/parameters_estimated_d1.json"

    ydata = get_data_simulation(est)['I']

    built_json, estimated_params = est.get_params_estimation_combine_infected(
        ydata)

    mse_for_params(estimated_params, [0.25, 0.052, 0.25, 0.052])
    save_file_as_json(paramas_estimated_json, built_json)


if __name__ == "__main__":
    main()
