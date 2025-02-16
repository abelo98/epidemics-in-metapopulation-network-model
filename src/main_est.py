from mmodel.params_estimation.estimator_class import estimator_SIR, estimator_SAIR
from mmodel.params_estimation.classic_models import estimator_SIR_classic, estimator_SAIR_classic
from mmodel.data_manager.data_operations import data_operator
from mmodel.json_manager.json_processor import *
from mmodel.constants import *
from cmodel.cmp.compile import compile_model
import os
import sys


def create_SEAIR():
    save_path = 'src/cmodel/repo'
    model = r"""
        \frac{dS}{dt} = - \frac{\beta ( I + A ) S}{N}\\
        \frac{dA}{dt} =  \frac{\beta ( I + A ) S}{N} - (\frac{1}{7}) A - \gamma A\\
        \frac{dI}{dt} = (\frac{1}{7}) A - \gamma I\\
        \frac{dR}{dt} = \gamma ( I + A )\\
        \frac{dN}{dt} = 0"""
    model_name = "SAIR"
    compile_model(text=model, model_name=model_name, path=save_path)


def select_model(nodes, network, params, iters, algorithem, initial_day, compartimrntal_type):
    if algorithem == 1:
        algorithem = 'pso'
    elif algorithem == 2:
        algorithem = 'diff_evol'
    else:
        algorithem = 'lm'

    if nodes > 1 and compartimrntal_type == 'SAIR':
        return estimator_SAIR(model_name=f"model_havana_d{initial_day}", network_path=network,
                              params_path=params, iter=iters, method=algorithem, numba=True, initial_day=initial_day)
    elif nodes > 1 and compartimrntal_type == 'SIR':
        return estimator_SIR(model_name=f"model_havana_d{initial_day}", network_path=network,
                             params_path=params, iter=iters, method=algorithem, numba=True, initial_day=initial_day)
    if nodes == 1 and compartimrntal_type == 'SAIR':
        return estimator_SAIR_classic(model_name=f"model_havana_d{initial_day}", network_path=network,
                                      params_path=params, iter=iters, method=algorithem, numba=True, initial_day=initial_day)
    elif nodes == 1 and compartimrntal_type == 'SIR':
        return estimator_SIR_classic(model_name=f"model_havana_d{initial_day}", network_path=network,
                                     params_path=params, iter=iters, method=algorithem, numba=True, initial_day=initial_day)


def make_estimation(network, params, result_location,
                    data_conf_path, data_dead_path, iters, algorithem, initial_day, nodes, model):

    est = select_model(nodes, network=network,
                       params=params, iters=iters, initial_day=initial_day, algorithem=algorithem, compartimrntal_type=model)

    d_op = data_operator(data_dead_path, data_conf_path)

    acc_infected = d_op.get_infected_by_muncps(params)

    new_paramas_to_save, time = est.get_params_estimation_combine_infected(
        acc_infected, d_op)

    print(f'elapsed time: {time} s')
    save_file_as_json(result_location, new_paramas_to_save)

    # if __name__ == "__main__":
    #     start_estimation()
    # create_SEAIR()
