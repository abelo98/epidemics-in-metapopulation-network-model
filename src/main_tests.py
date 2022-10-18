from locale import currency
from mmodel.params_estimation.estimate_params_test import estimator_test
from mmodel.json_manager.json_processor import *
import numpy as np
from mmodel.constants import *


def get_data_simulation(est: estimator_test, numba):
    days = np.linspace(0, 300, 300)
    return est.start_sim(days, numba)


def mse_for_params(params_est, real_params):
    mse = sum((params_est - real_params)**2)/len(real_params)
    return mse


def run_test():

    methods = ['pso', 'curve_fit', 'diff_evol']
    json_names = ['psoNumba', 'curve_fitNumba',
                  'diff_EvolNumba', 'pso', 'curve_fit', 'diff_Evol']
    with open("/media/abel/TERA/School/5to/Tesis/My work/correctness_fitting_functions.txt", "a") as f:

        for i, exec in enumerate(json_names):
            m = methods[i % len(json_names)]
            apply_numba = exec.__contains__('Numba')
            est = estimator_test(method=m, iter=6000)
            ydata = get_data_simulation(est, numba=apply_numba)['I']
            paramas_estimated_json = f"tests/mmodel/simple/estimation/parameters_estimated_{exec}_d1.json"
            print(" ", file=f)
            print(exec, file=f)
            print(" ", file=f)
            print(m, file=f)
            print("*********************************************", file=f)
            total_time = 0
            total_mse = 0
            best_mse = np.inf
            for _ in range(30):
                current_mse = 0
                built_json, estimated_params, crono = est.get_params_estimation_combine_infected(
                    ydata)
                total_time += crono
                current_mse = mse_for_params(
                    estimated_params, [0.25, 0.052, 0.25, 0.052])

                total_mse += current_mse

                if current_mse < best_mse:
                    best_mse = current_mse
                    save_file_as_json(paramas_estimated_json, built_json)

            print(" ", file=f)
            print(f"mean_time{total_time/30}", file=f)
            print(f"mean_time{total_mse/30}", file=f)
            print("*********************************************", file=f)
        f.close()


def main():
    run_test()
    # est = estimator_test(method='pso', iter=6000)

    # paramas_estimated_json = f"tests/mmodel/simple/estimation/parameters_estimated_pso_d1.json"

    # ydata = get_data_simulation(est)['I']

    # built_json, estimated_params, _ = est.get_params_estimation_combine_infected(
    #     ydata)

    # mse_for_params(estimated_params, [0.25, 0.052, 0.25, 0.052])
    # save_file_as_json(paramas_estimated_json, built_json)


if __name__ == "__main__":
    main()
