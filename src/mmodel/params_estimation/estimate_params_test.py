from ..api import ApiConn
from ..json_manager.json_processor import read_json
import numpy as np
from ..constants import START_INFECTED
from .calc_params import estimator_calc
from mmodel.data_manager.data_operations import data_operator


class estimator_test:
    def __init__(self, guess_path, model_name="", file_path="", params="", method='diff_evol'):
        self.model_name = "model_havana_d29"
        self.opt_func = None

        self.file_path = "tests/mmodel/simple/simple_network.json"
        self.params_path = "tests/mmodel/simple/params/simple_params.json"

        # compiles the model
        self.api = ApiConn(self.model_name, self.file_path)

        self.opt_func = estimator_calc(
            guess_path,  self.params_path, self.api, method)

    def start_sim(self, days):
        self.api.simulate(self.params_path, days)
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

    def get_initial_values_SIR_metamodel(self, models, infected):
        initial_v, guess = self.api.import_params(self.params_path)
        # its where the value of S is in the list for each muncp(order:S,I,R,N)
        i = 0
        time = len(infected)

        return initial_v, guess, np.linspace(0, time, time)

    def build_json_params_metamodel_combine(self, models_json, acc_infected_by_munc):
        output = []

        initial_v, guess, time = self.get_initial_values_SIR_metamodel(
            models_json, acc_infected_by_munc)
        muncps = [model["label"] for model in models_json]
        params_names = list(models_json[0]["params"].keys())

        new_params = self.opt_func.estimate_params_metamodel(
            acc_infected_by_munc, time, muncps, initial_v, guess, params_names)

        for i, model in enumerate(models_json):
            model["params"] = new_params[i]
            output.append(model)

        return output

    def get_params_estimation_combine_infected(self, infected):
        models = read_json(self.params_path)
        return self.build_json_params_metamodel_combine(models, infected)
