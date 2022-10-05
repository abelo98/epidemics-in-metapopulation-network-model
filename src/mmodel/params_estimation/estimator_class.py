from ..api import ApiConn
from ..json_manager.json_processor import read_json
import numpy as np
from ..constants import START_INFECTED
from .calc_params import estimator_calc


class estimator:
    def __init__(self, guess_path, model_name="", file_path="", params="", lmfit=False):
        self.model_name = "model_havana_d29"
        # self.file_path = "tests/mmodel/havana_metamodel_params_est/habana_network2.json"
        # self.params_path = "tests/mmodel/havana_metamodel_params_est/parameters_estimated_d16.json"
        self.opt_func = None
        self.file_path = "tests/mmodel/simple/one_node_network.json"
        self.params_path = "tests/mmodel/simple/params/simple_params_one_node.json"

        # self.file_path = "tests/mmodel/simple/simple_network.json"
        # self.params_path = "tests/mmodel/simple/params/simple_params.json"

        # compiles the model
        self.api = ApiConn(self.model_name, self.file_path)

        self.opt_func = estimator_calc(
            guess_path,  self.params_path, self.api, lmfit)

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

    def get_initial_values_SIR(self, json_file):
        S0 = json_file["y"]["S"]
        I0 = json_file["y"]["I"]
        R0 = json_file["y"]["R"]
        N = json_file["y"]["N"]

        return {"S": S0, "I": I0, "R": R0, "N": N}

    def set_initial_values(self, model, infected):
        initial_v = self.get_initial_values_SIR(model)
        infected_by_munc = infected[model["label"]][START_INFECTED:]
        munc = model["label"]
        time = np.linspace(0, len(infected_by_munc), len(infected_by_munc))
        id = int(model["id"])

        return initial_v, infected_by_munc, munc, time, id

    def build_json_params_metamodel(self, models_json, infected):
        output = []
        for model in models_json:
            _, infected_by_munc, munc, time, id = self.set_initial_values(
                model, infected)

            new_params = self.opt_func.estimate_params_metamodel(
                infected_by_munc, time, [munc], id)

            model["params"] = new_params[0]
            output.append(model)

        return output

    def build_json_params(self, models_json, infected):
        output = []
        for model in models_json:
            initial_v, infected_by_munc, munc, time, _ = self.set_initial_values(
                model, infected)

            new_params = self.opt_func.estimate_params_single_model(
                infected_by_munc, time, initial_v, munc)

            model["params"] = new_params
            output.append(model)

        return output

    def build_json_params_metamodel_combine(self, models_json, infected):
        output = []
        time = np.linspace(0, len(infected), len(infected))
        muncps = [model["label"] for model in models_json]

        new_params = self.opt_func.estimate_params_metamodel(
            infected, time, muncps, 0)

        for i, model in enumerate(models_json):
            model["params"] = new_params[i]
            output.append(model)

        return output

    def get_params_estimation(self, infected):
        models = read_json(self.params_path)
        return self.build_json_params(models, infected)

    def get_params_estimation_metamodel(self, infected):
        models = read_json(self.params_path)
        return self.build_json_params_metamodel(models, infected)

    def get_params_estimation_combine_infected(self, infected):
        models = read_json(self.params_path)
        return self.build_json_params_metamodel_combine(models, infected)
