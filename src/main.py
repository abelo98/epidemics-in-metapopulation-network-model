from mmodel.calc_params import estimate_params, initialize
from mmodel.data_reader import Reader
from mmodel.data_cleaner import Cleaner
import numpy as np
import json

{
    "id": 1,
    "label": "La Lisa",
    "model": "SIR",
    "y": {"S": 145022, "I": 1, "R": 0, "N": 145023},
    "params": {"beta": 0.17, "gamma": 0.082}
},


def get_initial_values(json_file):
    S0 = json_file["y"]["S"]
    I0 = json_file["y"]["I"]
    R0 = json_file["y"]["R"]
    N = json_file["y"]["N"]
    label = json_file["label"]

    return {label: [S0, I0, R0, N]}


def parse_params_pob_file(path, infected, params_to_estimate):
    with open(path, 'r') as f:
        json_parsed = json.load(f)
        for model in json_parsed:
            initail_v_and_label = get_initial_values(model)
            estimate(infected, params_to_estimate,initail_v_and_label)

        new_edges_json = []
        for edge in edges_json_file['graph']['edges']:
            current_perc = edge["metadata"]["weight"]
            munc_source = edge["source"]
            munc_target = edge["target"]
            real_portion_workers = current_perc * \
                amount_workers_per_munc[munc_source]
            real_perc_w = real_portion_workers/total_pop_per_munc[munc_source]
            new_edges_json.append({
                "source": munc_source,
                "target": munc_target,
                "metadata": {"weight": real_perc_w}
            })
        edges_json_file['edges'] = new_edges_json
        f.close()
    with open("tests/mmodel/network_correct_municipality_dist/habana_network2.json", 'w') as f:
        serialized_json = json.dumps(edges_json_file, indent=4)
        f.write(serialized_json)


def estimate(infected,params_to_estimate,initial_v:dict):
    print(initial_v.keys())
    print("params: ")
    print("")

    time = np.linspace(0, len(infected), len(infected))
    ydata = np.array(infected)
    
    estimate_params(ydata,time,params_to_estimate,initial_v)
    print("")



def main():
    data_conf_path = "/media/abel/TERA/School/5to/tesis stuff/cv19_conf_mun.xlsx"
    data_dead_path = "/media/abel/TERA/School/5to/tesis stuff/cv19_fall_mun.xlsx"

    muncps = ["Playa",
              "Plaza de la Revolución",
              "Centro Habana",
              "La Habana Vieja",
              "Regla",
              "La Habana del Este",
              "Guanabacoa",
              "San Miguel del Padrón",
              "Diez de Octubre",
              "Cerro",
              "Marianao",
              "La Lisa",
              "Boyeros",
              "Arroyo Naranjo",
              "Cotorro"]

    ydata = initialize()

    df_conf = Reader.get_data(data_conf_path)
    df_dead = Reader.get_data(data_dead_path)

    df_conf_havana = Cleaner.select_rows(df_conf, muncps)
    df_dead_havana = Cleaner.select_rows(df_dead, muncps)

    df_infected_havana = {
        key: abs(np.subtract(df_conf_havana[key], df_dead_havana[key])) for key in df_conf_havana}
