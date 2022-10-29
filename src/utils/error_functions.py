from mmodel.params_estimation.estimate_params_test import estimator_test
import numpy as np


def mse(params_est, real_params):
    output = sum((params_est - real_params)**2)/len(real_params)
    return output


def get_data_simulation(est: estimator_test, time, numba=False):
    days = np.linspace(0, time, time)
    return est.start_sim(days, numba)


def get_error(network, params_path_est, real_data):
    network = 'tests/mmodel/simple/simple_network.json'

    est = estimator_test(network_path=network, params=params_path_est,
                         method='curve_fit')

    ydata = get_data_simulation(est, time=len(real_data))['I']

    return mse(ydata, real_data)
