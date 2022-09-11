from .api import ApiConn
import numpy as np
import matplotlib.pyplot as plt
from scipy import integrate, optimize
from model import SIR

def get_ydata(caller: ApiConn, compartiments: list, idxs: list):
    output = {}
    for idx in idxs:
        for c in compartiments:
            output[c] = caller.get_ydata_for_node(idx, c).__next__()
    return output


def initialize(model_name="", file_path="", params="", days=None):
    model_name = "model_api"
    file_path = "tests/mmodel/network_correct_municipality_dist/habana_network2.json"
    params = "tests/mmodel/network_correct_municipality_dist/parameters.json"
    days = np.linspace(0, 200, 200)

    caller = ApiConn(model_name, file_path)
    caller.simulate(params, days)

    get_ydata(caller, ['S', 'I', 'R'], [0, 1])




def estimate_params(ydata: np.array, time: np.array, params: list,initial_v:dict):
    sir_model = SIR(initial_v)
    popt, pcov = optimize.curve_fit(sir_model.sir_ecuations, time, ydata)
    fitted = sir_model.fit_odeint(time, *popt)

    for i, p in enumerate(popt):
        print(f'{params[i]}: {p}')

    # plt.plot(time, ydata, 'o')
    # plt.plot(time, fitted)
    # plt.show()


N = 1.0
I0 = ydata[0]
S0 = N - I0
R0 = 0.0
