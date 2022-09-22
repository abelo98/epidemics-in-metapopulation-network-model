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
