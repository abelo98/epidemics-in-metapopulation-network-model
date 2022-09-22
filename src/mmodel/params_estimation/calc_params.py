from ..data_manager.api import ApiConn
from ..json_manager.json_processor import read_json
import numpy as np
from scipy import integrate, optimize
from .model import SIR
from ..constants import BETA, GAMMA, START_INFECTED
from ....tests.mmodel.simple.model_api_network_2_nodes import deriv


class estimator:
    def __init__(self, model_name="", file_path="", params="", days=0):
        self.model_name = "model_api_network_2_nodes"
        self.file_path = "tests/mmodel/simple/simple_network.json"
        self.params = "tests/mmodel/simple/params/simple_params.json"
        self.days = np.linspace(0, days, days)

        self.api = ApiConn(self.model_name, self.file_path)

    def start_sim(self):
        self.api.simulate(self.params, self.days)
        self.get_ydata(self.api, ['S', 'I', 'R'], [0, 1])

    i_values = None

    def get_ydata(caller: ApiConn, compartiments: list, idxs: list):
        output = {}
        for idx in idxs:
            for c in compartiments:
                output[c] = caller.get_ydata_for_node(idx, c).__next__()
        return output

    def __get_params__(self, params, munc, popt):
        params_estimated = {}
        for i, p in enumerate(popt):
            print(munc)
            print("params: ")
            print("")
            print(f'{params[i]}: {p}')
            params_estimated[params[i]] = p
        return params_estimated

    @staticmethod
    def fit_odeint(i_values, x, beta, gamma):
        return integrate.odeint(SIR.sir_ecuations, i_values, x, args=(beta, gamma))[:, 1]

    @staticmethod
    def fit_odeint_metamodel(i_values, x, params):
        return integrate.odeint(deriv, i_values, x, args=(params,))[:, 1]

    def estimate_params_metamodel(self, ydata: np.array, time: np.array, params: list, initial_v: dict, munc):
        global i_values
        i_values = [initial_v.values()]
        i_values = self.api.transform_input(i_values)

        popt, _ = optimize.curve_fit(
            estimator.fit_odeint_metamodel, time, ydata, bounds=(0, 1), maxfev=5000)

        return self.__get_params__(params, munc, popt)

    def estimate_params(self, ydata: np.array, time: np.array, params: list, initial_v: dict, munc):
        global i_values
        i_values = tuple(initial_v.values())

        popt, _ = optimize.curve_fit(estimator.fit_odeint_metamodel, time, ydata, p0=[
            BETA, GAMMA], bounds=(0, 1), maxfev=5000)

        return self.__get_params__(params, munc, popt)

    def get_initial_values_SIR(json_file):
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

        return initial_v, infected_by_munc, munc, time

    def build_json_params_metamodel(self, models_json, infected, params_to_estimate):
        output = []
        for model in models_json:
            initial_v, infected_by_munc, munc, time = self.set_initial_values(
                model, infected)

            new_params = self.estimate_params_metamodel(
                infected_by_munc, time, params_to_estimate, initial_v, munc)

            model["params"] = new_params
            output.append(model)

        return output

    def build_json_params(self, models_json, infected, params_to_estimate):
        output = []
        for model in models_json:
            initial_v, infected_by_munc, munc, time = self.set_initial_values(
                model, infected)

            new_params = self.estimate_params(
                infected_by_munc, time, params_to_estimate, initial_v, munc)

            model["params"] = new_params
            output.append(model)

        return output

    def get_params_estimation(self, nodes_params_json_path, infected, params_to_estiamte):
        models = read_json(nodes_params_json_path)
        return self.build_json_params(models, infected, params_to_estiamte)

    def get_params_estimation_metamodel(self, nodes_params_json_path, infected, params_to_estiamte):
        models = read_json(nodes_params_json_path)
        return self.build_json_params_metamodel(models, infected, params_to_estiamte)
