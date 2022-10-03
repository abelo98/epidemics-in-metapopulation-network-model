from ..api import ApiConn
from ..json_manager.json_processor import read_json
import numpy as np
from scipy import integrate, optimize
from .model import SIR
from ..constants import BETA, GAMMA, START_INFECTED


class estimator:
    def __init__(self, model_name="", file_path="", params="", days=0):
        self.model_name = "model_havana_d29"
        self.file_path = "tests/mmodel/havana_metamodel_params_est/habana_network2.json"
        self.params_path = "tests/mmodel/havana_metamodel_params_est/parameters_estimated_d16.json"
        # self.file_path = "tests/mmodel/simple/simple_network.json"

        # self.params_path = "tests/mmodel/simple/params/simple_params.json"

        self.days = np.linspace(0, days, days)

        # compiles the model
        self.api = ApiConn(self.model_name, self.file_path)

        # self.start_sim()

    def start_sim(self):
        self.api.simulate(self.params_path, self.days)
        self.get_ydata(self.api, ['S', 'I', 'R'], [0, 1])

    i_values = None
    metamodel = None

    def get_ydata(self, caller: ApiConn, compartiments: list, idxs: list):
        output = {}
        for idx in idxs:
            for c in compartiments:
                output[c] = caller.get_ydata_for_node(idx, c).__next__()
        return output

    def __get_params__(self, params, muncps, popt, id=0):
        params_estimated = []

        for id, munc in enumerate(muncps):
            start = id*len(params)
            end = start+len(params)
            estimation = {}

            print(munc)
            print("params: ")
            for i, p in enumerate(popt[start:end]):
                print(f'{params[i%len(params)]}: {p}')
                estimation[params[i % len(params)]] = p
            params_estimated.append(estimation)
            print("")
        return params_estimated

    @ staticmethod
    def fit_odeint(x, beta, gamma):
        return integrate.odeint(SIR.sir_ecuations, i_values, x, args=(beta, gamma))[:, 1]

    @ staticmethod
    def fit_odeint_metamodel(x, *params):
        return integrate.odeint(metamodel.deriv, i_values, x, args=(params,))[:, 1]

    def estimate_params_metamodel(self, ydata: np.array, time: np.array, params: list, muncps: list, id=0):
        global i_values
        i_values, _ = self.api.import_params(self.params_path)
        i_values = self.api.transform_input(i_values)

        # imports the metamodel
        global metamodel
        metamodel = self.api.import_model(
            self.api.model.name, self.api.model.code_file)

        # TODO: need to change the code below to accept a list of estimation
        guess = []
        for i in range(0, 30):
            if i % 2 == 0:
                guess.append(BETA)
            else:
                guess.append(GAMMA)

        popt, _ = optimize.curve_fit(
            estimator.fit_odeint_metamodel, time, ydata, p0=guess, maxfev=5000)

        return self.__get_params__(params, muncps, popt, id)

    def estimate_params(self, ydata: np.array, time: np.array, params: list, initial_v: dict, munc):
        global i_values
        i_values = tuple(initial_v.values())

        popt, _ = optimize.curve_fit(estimator.fit_odeint, time, ydata, p0=[
            BETA, GAMMA], maxfev=5000)

        return self.__get_params__(params, [munc], popt)

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

    def build_json_params_metamodel(self, models_json, infected, params_to_estimate):
        output = []
        for model in models_json:
            _, infected_by_munc, munc, time, id = self.set_initial_values(
                model, infected)

            new_params = self.estimate_params_metamodel(
                infected_by_munc, time, params_to_estimate, [munc], id)

            model["params"] = new_params[0]
            output.append(model)

        return output

    def build_json_params_metamodel_combine(self, models_json, infected, params_to_estimate):
        output = []
        time = np.linspace(0, len(infected), len(infected))
        muncps = [model["label"] for model in models_json]

        new_params = self.estimate_params_metamodel(
            infected, time, params_to_estimate, muncps, 0)

        for i, model in enumerate(models_json):
            model["params"] = new_params[i]
            output.append(model)

        return output

    def build_json_params(self, models_json, infected, params_to_estimate):
        output = []
        for model in models_json:
            initial_v, infected_by_munc, munc, time, _ = self.set_initial_values(
                model, infected)

            new_params = self.estimate_params(
                infected_by_munc, time, params_to_estimate, initial_v, munc)

            model["params"] = new_params
            output.append(model)

        return output

    def get_params_estimation(self, infected, params_to_estiamte):
        models = read_json(self.params_path)
        return self.build_json_params(models, infected, params_to_estiamte)

    def get_params_estimation_metamodel(self, infected, params_to_estiamte):
        models = read_json(self.params_path)
        return self.build_json_params_metamodel(models, infected, params_to_estiamte)

    def get_params_estimation_combine_infected(self, infected, params_to_estiamte):
        models = read_json(self.params_path)
        return self.build_json_params_metamodel_combine(
            models, infected, params_to_estiamte)
