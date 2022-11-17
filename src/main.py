from mmodel.params_estimation.estimator_class import estimator_SIR, estimator_SEAIR
from mmodel.data_manager.data_operations import data_operator
from mmodel.json_manager.json_processor import *
from mmodel.constants import *
from cmodel.cmp.compile import compile_model
import os
import sys


def calc_params_with_acc_infected_combine(est: estimator_SIR, acc_infected, d_op):
    return est.get_params_estimation_combine_infected(acc_infected, d_op)


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
    iters = 10000
    networks = [
        'tests/mmodel/havana_geo_connections SEAIR/havana_geo_correct_perc.json']

    params = [
        'tests/mmodel/havana_geo_connections SEAIR/params/parameters_d16.json']

    paramas_estimated_jsons = [
        f"tests/mmodel/havana_geo_connections SEAIR/estimation/parameters_estimated_pso_SEAIR_Numba_GPU_d{START_INFECTED}_iter-{iters}.json"]

    data_conf_path = "data_cov/cv19_conf_mun.xlsx"
    data_dead_path = "data_cov/cv19_fall_mun.xlsx"
    results_path = os.path.join(os.path.abspath(
        os.getcwd()), "out_DE.txt")

    with open(results_path, "a") as sys.stdout:

        for i, n in enumerate(networks):
            est = estimator_SEAIR(model_name=f"model_havana_d{START_INFECTED}", network_path=n,
                                  params_path=params[i], iter=iters, method='pso', numba=True)

            d_op = data_operator(data_dead_path, data_conf_path)

            acc_infected = d_op.get_infected_by_muncps(params[i])

            new_paramas_to_save, time = calc_params_with_acc_infected_combine(
                est, acc_infected, d_op)

            print(f'elapsed time: {time} s')
            save_file_as_json(paramas_estimated_jsons[i], new_paramas_to_save)

    # os.system("shutdown /s /t 1")


if __name__ == "__main__":
    # main()
    create_SEAIR()
