from ..api import ApiConn
from ..json_manager.json_processor import read_json
import numpy as np
from .calc_params import estimator_calc
from ..constants import GUESS


class estimator_test:
    def __init__(self, model_name="model_havana_d29", network_path="", params="", method='diff_evol', iter=6000, numba=False):
        self.opt_func = None
        self.params_path = params
        self.network_path = network_path
        self.model_name = model_name
        self.method = method
        self.iter = iter
        # compiles the model
        self.api = ApiConn(self.model_name, self.network_path, numba)

    def start_sim(self, days, numba):
        self.api.simulate(self.params_path, days, numba)
        return self.__get_ydata__()

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

    def get_initial_values_SIR_metamodel(self, infected):
        initial_v, guess = self.api.import_params(self.params_path)
        guess = GUESS
        time = len(infected)

        return initial_v, guess, np.linspace(0, time, time)

    def build_json_params_metamodel_combine(self, models_json, acc_infected_by_munc):
        opt_func = estimator_calc(self.api, self.method, iter=self.iter)
        output = []

        initial_v, guess, time = self.get_initial_values_SIR_metamodel(
            acc_infected_by_munc)

        muncps = [model["label"] for model in models_json]
        params_names = list(models_json[0]["params"].keys())

        new_params, crono = opt_func.estimate_params_metamodel(
            acc_infected_by_munc, time, muncps, initial_v, guess, params_names)

        for i, model in enumerate(models_json):
            model["params"] = new_params[i]
            output.append(model)

        return output, new_params, crono

    def get_params_estimation_combine_infected(self, infected):
        models = read_json(self.params_path)
        return self.build_json_params_metamodel_combine(models, infected)
