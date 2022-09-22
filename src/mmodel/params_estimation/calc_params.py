from ..data_manager.api import ApiConn
from ..json_manager.json_processor import read_json
import numpy as np
from scipy import integrate, optimize
from .model import SIR
from ...constants import *

i_values = None


def get_ydata(caller: ApiConn, compartiments: list, idxs: list):
    output = {}
    for idx in idxs:
        for c in compartiments:
            output[c] = caller.get_ydata_for_node(idx, c).__next__()
    return output


def initialize(model_name="", file_path="", params="", days=None):
    model_name = "model_api_network_2_nodes"
    file_path = "tests/mmodel/simple/simple_network.json"
    params = "tests/mmodel/simple/params/simple_params.json"
    days = np.linspace(0, 200, 200)

    caller = ApiConn(model_name, file_path)
    caller.simulate(params, days)

    get_ydata(caller, ['S', 'I', 'R'], [0, 1])


def fit_odeint(i_values, x, beta, gamma):
    return integrate.odeint(SIR.sir_ecuations, i_values, x, args=(beta, gamma))[:, 1]


def estimate_params(ydata: np.array, time: np.array, params: list, initial_v: dict, munc):
    global i_values
    i_values = tuple(initial_v.values())

    popt, _ = optimize.curve_fit(fit_odeint, time, ydata, p0=[
                                 BETA, GAMMA], bounds=(0, 1), maxfev=5000)

    params_estimated = {}
    for i, p in enumerate(popt):
        print(munc)
        print("params: ")
        print("")
        print(f'{params[i]}: {p}')
        params_estimated[params[i]] = p

    return params_estimated


def get_initial_values_SIR(json_file):
    S0 = json_file["y"]["S"]
    I0 = json_file["y"]["I"]
    R0 = json_file["y"]["R"]

    return {"S": S0, "I": I0, "R": R0}


def build_json_params(models_json, infected, params_to_estimate):
    output = []
    for model in models_json:
        initial_v = get_initial_values_SIR(model)
        infected_by_munc = infected[model["label"]][START_INFECTED:]
        munc = model["label"]
        time = np.linspace(0, len(infected_by_munc), len(infected_by_munc))

        new_params = estimate_params(
            infected_by_munc, time, params_to_estimate, initial_v, munc)

        model["params"] = new_params
        output.append(model)

    return output


def get_params_estimation(params_json_path, infected, params_to_estiamte):
    models = read_json(params_json_path)
    return build_json_params(models, infected, params_to_estiamte)
