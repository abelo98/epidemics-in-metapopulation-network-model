from ..api import ApiConn
from ..json_manager.json_processor import read_json
import numpy as np
from ..constants import START_INFECTED
from .calc_params import estimator_calc
from mmodel.data_manager.data_operations import data_operator


class estimator:
    def __init__(self, guess_path, model_name="", file_path="", params="", lmfit=False):
        self.model_name = "model_havana_d29"

        # self.file_path = "tests/mmodel/test_network_habana_vieja_and_its_connections/network.json"
        # self.params_path = "tests/mmodel/test_network_habana_vieja_and_its_connections/params/parameters_estimated_d16.json"

        self.file_path = "tests/mmodel/havana_full_network/network.json"
        self.params_path = "tests/mmodel/havana_full_network/params/parameters_d16.json"
        self.opt_func = None
        # self.file_path = "tests/mmodel/simple/one_node_network.json"
        # self.params_path = "tests/mmodel/simple/params/simple_params_one_node.json"

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

    def get_initial_values_SIR(self, infected_by_munc, json_file):
        I0 = infected_by_munc[0]
        S0 = json_file["y"]["N"] - I0
        R0 = json_file["y"]["R"]
        N = json_file["y"]["N"]

        p1 = json_file["params"]["beta"]
        p2 = json_file["params"]["gamma"]

        return {"S": S0, "I": I0, "R": R0, "N": N}, [p1, p2]

    def get_initial_values_SIR_metamodel(self, models, infected):
        initial_v, guess = self.api.import_params(self.params_path)
        # its where the value of S is in the list for each muncp(order:S,I,R,N)
        i = 0
        time = -np.inf
        for model in models:
            infected_by_munc = infected[model["label"]][START_INFECTED:]
            if (len(infected_by_munc) > time):
                time = len(infected_by_munc)

            initial_v[i] = initial_v[i+3] - infected_by_munc[0]
            initial_v[i+1] = infected_by_munc[0]
            i += 4  # where the initial values of other munc start

        return initial_v, guess, np.linspace(0, time, time)

    def set_initial_values(self, model, infected):
        infected_by_munc = infected[model["label"]][START_INFECTED:]
        munc = model["label"]
        time = np.linspace(0, len(infected_by_munc), len(infected_by_munc))
        id = int(model["id"])

        return infected_by_munc, munc, time, id

    # def build_json_params_metamodel(self, models_json, infected):
    #     output = []

    #     initial_v, guess = self.get_initial_values_SIR_metamodel(
    #         models_json, infected)

    #     for model in models_json:
    #         params_names = model["params"].values()

    #         infected_by_munc, munc, time, id = self.set_initial_values(
    #             model, infected)

    #         new_params = self.opt_func.estimate_params_metamodel(
    #             infected_by_munc, time, [munc], initial_v, guess, params_names, id)

    #         model["params"] = new_params[0]  # revisar esto
    #         output.append(model)

    #     return output

    def build_json_params(self, models_json, infected):
        output = []
        for model in models_json:
            params_names = model["params"].values()

            initial_v, guess = self.get_initial_values_SIR(
                infected_by_munc, model)

            infected_by_munc, munc, time, _ = self.set_initial_values(
                model, infected)

            new_params = self.opt_func.estimate_params_single_model(
                infected_by_munc, time, initial_v, guess, params_names, munc)

            model["params"] = new_params
            output.append(model)

        return output

    def build_json_params_metamodel_combine(self, models_json, acc_infected_by_munc):
        output = []
        acc_infected_combine = data_operator.combine_infected_all_mcps(
            acc_infected_by_munc)[START_INFECTED:]
        initial_v, guess, time = self.get_initial_values_SIR_metamodel(
            models_json, acc_infected_by_munc)
        muncps = [model["label"] for model in models_json]
        params_names = list(models_json[0]["params"].keys())

        new_params = self.opt_func.estimate_params_metamodel(
            acc_infected_combine, time, muncps, initial_v, guess, params_names, 0)

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
