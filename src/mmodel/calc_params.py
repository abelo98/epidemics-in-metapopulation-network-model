from .api import ApiConn
import numpy as np

def get_ydata(caller: ApiConn, compartiments: list, idxs: list):
    output = {}
    for idx in idxs:
        for c in compartiments:
            output[c] = caller.get_ydata_for_node(idx, c).__next__()
    return output

def Initialized(model_name = "", file_path="", params="", days=None):
    model_name = "model_api"
    file_path = "tests/mmodel/network_correct_municipality_dist/habana_network2.json"
    params = "tests/mmodel/network_correct_municipality_dist/parameters.json"
    days = np.linspace(0, 200, 200)

    caller = ApiConn(model_name, file_path)
    caller.simulate(params, days)

    get_ydata(caller, ['S', 'I', 'R'], [0, 1])

