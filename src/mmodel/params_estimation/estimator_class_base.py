from ..api import ApiConn
from .calc_params import *


class estimator_base:
    def __init__(self, model_name: str, network_path: str, params_path: str, method='diff_evol', iter=6000, numba=False, initial_day=1):
        self.model_name = model_name
        self.params_path = params_path
        self.method_name = method
        self.iter = iter
        self.initial_day = initial_day
        # compiles the model
        self.api = ApiConn(self.model_name, network_path, numba)
        self.opt_func = self.__opt_selector__()

    def start_sim(self, days, numba):
        self.api.simulate(self.params_path, days, numba)
        return self.__get_ydata__()

    def __opt_selector__(self):
        if self.method_name == 'pso':
            return estimator_calc_PSO(self.api, self.iter)
        elif self.method_name == 'lm':
            return estimator_calc_LM(self.api, self.iter)

        return estimator_calc_Diff_Evol(self.api, self.iter)

    def __get_ydata__(self):
        output = {}
        nodes = self.api.get_network_nodes()
        for node in nodes:
            for c in node.cmodel:
                try:
                    output[c] += self.api.get_ydata_for_node(
                        node.id, c).__next__()
                except KeyError:
                    output[c] = self.api.get_ydata_for_node(
                        node.id, c).__next__()
        return output

    def get_initial_values_metamodel(self, models, infected):
        raise NotImplementedError()

    def build_json_params_metamodel(self, models_json, acc_infected_by_munc, d_op):
        raise NotImplementedError()

    def get_params_estimation_combine_infected(self, infected, d_op):
        raise NotImplementedError()
