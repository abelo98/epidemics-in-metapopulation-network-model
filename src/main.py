from mmodel.calc_params import estimate_params, initialize
from mmodel.data_reader import Reader
from mmodel.data_cleaner import Cleaner
import numpy as np
import json


def get_initial_values(json_file):
    S0 = json_file["y"]["S"]
    I0 = json_file["y"]["I"]
    R0 = json_file["y"]["R"]
    N = json_file["y"]["N"]

    return {"S": S0, "I": I0, "R": R0, "N": N}


def estimate_new_params(current_paramas_json, infected, params_to_estimate):
    with open(current_paramas_json, 'r') as f:
        json_parsed = json.load(f)
        output = []
        for model in json_parsed:
            initail_v_and_label = get_initial_values(model)
            infected_by_munc = infected[model["label"]][15:]
            munc = model["label"]
            new_params = call_estimator(
                munc, infected_by_munc, params_to_estimate, initail_v_and_label)
            model["params"] = new_params
            output.append(model)
        f.close()
        return output


def save_file_as_json(path, file: list):
    with open(path, 'w') as f:
        serialized_json = json.dumps(file, indent=4)
        f.write(serialized_json)
        f.close()


def call_estimator(munc,infected, params_to_estimate, initial_v: dict):
    print(munc)
    print("params: ")
    print("")

    time = np.linspace(0, len(infected), len(infected))
    ydata = np.array(infected)

    return estimate_params(ydata, time, params_to_estimate, initial_v)


def main():
    data_conf_path = "/media/abel/TERA/School/5to/tesis stuff/cv19_conf_mun.xlsx"
    data_dead_path = "/media/abel/TERA/School/5to/tesis stuff/cv19_fall_mun.xlsx"
    current_paramas_json = "/media/abel/TERA/School/5to/Tesis/My work/epidemics-in-metapopulation-network-model/tests/mmodel/network_correct_municipality_dist/parameters_d16.json"
    paramas_estimated_json = "/media/abel/TERA/School/5to/Tesis/My work/epidemics-in-metapopulation-network-model/tests/mmodel/network_correct_municipality_dist/parameters_estimated_d16.json"

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

    # ydata = initialize()

    df_conf = Reader.get_data(data_conf_path)
    df_dead = Reader.get_data(data_dead_path)

    df_conf_havana = Cleaner.select_rows(df_conf, muncps)
    df_dead_havana = Cleaner.select_rows(df_dead, muncps)

    df_infected_havana = {
        key: abs(np.subtract(df_conf_havana[key], df_dead_havana[key])) for key in df_conf_havana}

    new_paramas_to_save = estimate_new_params(current_paramas_json,
                                              df_infected_havana, ["beta", "gamma"])

    save_file_as_json(paramas_estimated_json, new_paramas_to_save)


if __name__ == "__main__":
    main()
