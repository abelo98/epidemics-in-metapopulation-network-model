from mmodel.params_estimation.estimator_class import estimator_SIR, estimator_SAIR
from mmodel.params_estimation.classic_models import estimator_SIR_classic, estimator_SAIR_classic
from mmodel.data_manager.data_operations import data_operator
from mmodel.json_manager.json_processor import *
from mmodel.constants import *
from cmodel.cmp.compile import compile_model
import os
import sys


# def calc_params_with_acc_infected_combine(est: estimator_SIR, acc_infected, d_op):
#     return est.get_params_estimation_combine_infected(acc_infected, d_op)


def create_SEAIR():
    save_path = 'src/cmodel/repo'
    text = r"""
            \frac{dS}{dt} = - \frac{\beta S I}{N}\\
            \frac{dI}{dt} = \frac{\beta S I}{N} - \gamma I\\
            \frac{dR}{dt} = \gamma I
            """
    model = r"""
        \frac{dS}{dt} = - \frac{\beta ( I + A ) S}{N}\\
        \frac{dA}{dt} =  \frac{\beta ( I + A ) S}{N} - (\frac{1}{7}) A - \gamma A\\
        \frac{dI}{dt} = (\frac{1}{7}) A - \gamma I\\
        \frac{dR}{dt} = \gamma ( I + A )\\
        \frac{dN}{dt} = 0"""
    model_name = "SAIR"
    compile_model(text=model, model_name=model_name, path=save_path)


def main():
    iters = 20000
    networks = ['tests/mmodel/havana_geo_connections/havana_geo_correct_perc.json',
                'tests/mmodel/havana_all_connections/havana_network_correct_perc.json',
                'tests/mmodel/without_centro_habana_all_connections/havana_network_correct_perc.json',
                'tests/mmodel/without_plaza_all_connections/havana_network_correct_perc.json']

    params = ['tests/mmodel/havana_geo_connections/estimation/parameters_estimated_PSO_Numba_GPU_d29_iter-50000.json',
              'tests/mmodel/havana_all_connections/estimation/parameters_estimated_PSO_Numba_GPU_d29_iter-50000.json',
              'tests/mmodel/without_centro_habana_all_connections/estimation/parameters_estimated_PSO_Numba_GPU_d29_iter-50000.json',
              'tests/mmodel/without_plaza_all_connections/estimation/parameters_estimated_PSO_Numba_d29_iter-50000.json']

    paramas_estimated_jsons = [
        'tests/mmodel/havana_geo_connections/estimation/estimation_PSO_Numba_2_d29_iter-50000.json',
        'tests/mmodel/havana_all_connections/estimation/estimation_PSO_Numba_2_d29_iter-50000.json',
        'tests/mmodel/without_centro_habana_all_connections/estimation/estimation_PSO_Numba_2_d29_iter-50000.json',
        'tests/mmodel/without_plaza_all_connections/estimation/estimation_PSO_Numba_2_d29_iter-50000.json'
    ]

    data_conf_path = "data_cov/cv19_conf_mun.xlsx"
    data_dead_path = "data_cov/cv19_fall_mun.xlsx"
    results_path = os.path.join(os.path.abspath(
        os.getcwd()), "out_All_models.txt")

    with open(results_path, "a") as sys.stdout:

        for i, n in enumerate(networks):
            est = estimator_SIR(model_name=f"model_havana_d{START_INFECTED}", network_path=n,
                                params_path=params[i], iter=iters, method='pso', numba=True)

            d_op = data_operator(data_dead_path, data_conf_path)

            acc_infected = d_op.get_infected_by_muncps(params[i])

            new_paramas_to_save, time = est.get_params_estimation_combine_infected(
                acc_infected, d_op)

            print(f'elapsed time: {time} s')
            save_file_as_json(paramas_estimated_jsons[i], new_paramas_to_save)

    # os.system("shutdown /s /t 1")


if __name__ == "__main__":
    main()
    # create_SEAIR()
