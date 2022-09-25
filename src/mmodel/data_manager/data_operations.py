import numpy as np


class data_operator:
    @staticmethod
    def get_conf_less_dead(df_conf_havana: dict, df_dead_havana: dict):
        return {
            key: np.subtract(df_conf_havana[key], df_dead_havana[key]) for key in df_conf_havana}

    @staticmethod
    def calc_infected(conf_less_dead: dict):
        infected = {}

        for munc in conf_less_dead:
            accumaleted_infected = []
            for idx in range(0, len(conf_less_dead[munc])):
                accumaleted_infected.append(sum(conf_less_dead[munc][0:idx]))
            infected[munc] = accumaleted_infected

        return infected

    @staticmethod
    def __find_min__(acc_infected_by_mcp: dict):
        min = -1000000
        for k, v in acc_infected_by_mcp:
            if len(acc_infected_by_mcp[k]) > min:
                min = len(acc_infected_by_mcp[k])
        return min

    @staticmethod
    def combine_infected_all_mcps(acc_infected_by_mcp: dict):
        output = []
        max_days = data_operator.__find_min__(acc_infected_by_mcp)

        for i in range(0, max_days):
            acc = 0
            for list_infected_by_day in acc_infected_by_mcp.values():
                acc += list_infected_by_day[i]
            output.append(acc)
        return output
