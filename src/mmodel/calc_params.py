from .api import ApiConn
import numpy as np

def get_ydata(caller:ApiConn, compartiments:list, idxs:list):
    result = {}
    for idx in idxs:
        for c in compartiments:
            result[c] = caller.get_ydata_for_node(idx,c).__next__()
            print(result[c])

def main():
    model_name = "model_api"
    file_path = "tests/mmodel/network_correct_municipality_dist/habana_network2.json"
    params = "tests/mmodel/network_correct_municipality_dist/parameters.json"
    days = np.linspace(0, 200, 200)

    caller = ApiConn(model_name,file_path)
    caller.simulate(params,days)

    get_ydata(caller, ['S','I','R'],[0,1])
    

if __name__ == "__main__":
    main()