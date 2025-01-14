import numpy as np

from mmodel.json_manager.json_processor import read_json
from .data_reader import Reader
from .data_cleaner import Cleaner


class data_operator:
    def __init__(self, death_path: str, confirmed_path: str) -> None:
        self.death_path = death_path
        self.confirmed_path = confirmed_path

    def __get_conf_less_dead__(self, df_conf_havana: dict, df_dead_havana: dict):
        return {
            key: np.subtract(df_conf_havana[key], df_dead_havana[key]) for key in df_conf_havana}

    def __calc_infected__(self, conf_less_dead: dict):
        infected = {}

        for munc in conf_less_dead:
            accumaleted_infected = []
            for idx in range(0, len(conf_less_dead[munc])):
                accumaleted_infected.append(sum(conf_less_dead[munc][0:idx]))
            infected[munc] = accumaleted_infected

        return infected

    def __find_min__(self, acc_infected_by_mcp: dict):
        min = -1000000
        for k, _ in acc_infected_by_mcp.items():
            if len(acc_infected_by_mcp[k]) > min:
                min = len(acc_infected_by_mcp[k])
        return min

    def combine_infected_all_mcps(self, acc_infected_by_mcp: dict):
        output = []
        max_days = self.__find_min__(acc_infected_by_mcp)

        for i in range(0, max_days):
            acc = 0
            for list_infected_by_day in acc_infected_by_mcp.values():
                acc += list_infected_by_day[i]
            output.append(acc)
        return output

    def get_infected_by_muncps(self, params_path):
        df_conf_havana = self.__get_data_from_path__(
            params_path, self.confirmed_path)

        df_dead_havana = self.__get_data_from_path__(
            params_path, self.death_path)

        df_conf_less_dead_havana = self.__get_conf_less_dead__(
            df_conf_havana, df_dead_havana)

        acc_infected = self.__calc_infected__(df_conf_less_dead_havana)

        return acc_infected

    def __get_data_from_path__(self, params_path, data_path):
        df_data = Reader.get_data(data_path)

        models = read_json(params_path)
        muncps = [model["label"] for model in models]

        return Cleaner.select_rows(df_data, muncps)

    def get_deaths_all_combine(self, params_path):
        df_dead_havana = self.__get_data_from_path__(
            params_path, self.death_path)

        output = np.zeros(self.__find_min__(df_dead_havana), dtype=np.int64)
        for i in range(len(output)):
            for l in df_dead_havana.values():
                output[i] += l[i]

        return output
