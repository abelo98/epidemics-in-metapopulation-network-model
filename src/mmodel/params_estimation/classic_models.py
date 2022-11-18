from ..json_manager.json_processor import read_json
import numpy as np
from ..constants import START_INFECTED
from .estimator_class_base import estimator_base


class estimator_SIR_classic(estimator_base):
    def get_initial_values_metamodel(self, models, infected):
        initial_v, guess = self.api.import_params(self.params_path)
        guess = guess[:2]
        # its where the value of S is in the list for each muncp(order:S,I,R,N)
        time = -np.inf
        index_N = len(models[0]['model'])
        index_S = models[0]['model'].index('S')
        total_popultaion = 0
        total_susceptibles = 0
        total_infected = 0

        for model in models:
            total_infected += infected[model["label"]][START_INFECTED]

            infected_by_munc = infected[model["label"]][START_INFECTED:]
            if (len(infected_by_munc) > time):
                time = len(infected_by_munc)

            total_popultaion += initial_v[index_S + index_N]
            total_susceptibles += initial_v[index_S +
                                            index_N] - infected_by_munc[0]

            # where the initial values of other munc start
            index_S += len(model["y"])

        return [total_susceptibles, total_infected, 0, total_popultaion], guess, np.linspace(0, time, time)

    def build_json_params_metamodel(self, models_json, acc_infected_by_munc, d_op):
        output = []
        acc_infected_combine = d_op.combine_infected_all_mcps(
            acc_infected_by_munc)[START_INFECTED:]

        initial_v, guess, time = self.get_initial_values_metamodel(
            models_json, acc_infected_by_munc)

        muncps = ["Habana"]

        params_names = list(models_json[0]["params"].keys())[:2]

        new_params, time = self.opt_func.estimate_params_metamodel(
            acc_infected_combine, time, muncps, initial_v, guess, params_names)

        models_json[0]["params"] = new_params[0]
        models_json[0]["label"] = "Habana"
        models_json[0]["y"]["S"] = int(initial_v[0])
        models_json[0]["y"]["I"] = int(initial_v[1])
        models_json[0]["y"]["R"] = int(initial_v[2])
        models_json[0]["y"]["N"] = int(initial_v[3])

        output.append(models_json[0])

        return output, time

    def get_params_estimation_combine_infected(self, infected, d_op):
        models = read_json(self.params_path)
        return self.build_json_params_metamodel(models, infected, d_op)


class estimator_SAIR_classic(estimator_base):
    def get_initial_values_metamodel(self, models, infected):
        initial_v, guess = self.api.import_params(self.params_path)
        guess = guess[:2]
        # its where the value of S is in the list for each muncp(order:S,A,I,R,N)
        time = -np.inf
        index_N = len(models[0]['model'])
        index_S = models[0]['model'].index('S')
        total_popultaion = 0
        total_susceptibles = 0
        total_infected = 0

        for model in models:
            total_infected += infected[model["label"]][START_INFECTED]

            infected_by_munc = infected[model["label"]][START_INFECTED:]
            if (len(infected_by_munc) > time):
                time = len(infected_by_munc)

            total_popultaion += initial_v[index_S + index_N]
            total_susceptibles += initial_v[index_S +
                                            index_N] - infected_by_munc[0]

            # where the initial values of other munc start
            index_S += len(model["y"])

        return [total_susceptibles, 0, total_infected, 0, total_popultaion], guess, np.linspace(0, time, time)

    def build_json_params_metamodel(self, models_json, acc_infected_by_munc, d_op):
        output = []
        acc_infected_combine = d_op.combine_infected_all_mcps(
            acc_infected_by_munc)[START_INFECTED:]

        initial_v, guess, time = self.get_initial_values_metamodel(
            models_json, acc_infected_by_munc)

        muncps = ["Habana"]

        params_names = list(models_json[0]["params"].keys())[:2]

        new_params, time = self.opt_func.estimate_params_metamodel(
            acc_infected_combine, time, muncps, initial_v, guess, params_names)

        models_json[0]["params"] = new_params[0]
        models_json[0]["label"] = "Habana"
        models_json[0]["y"]["S"] = int(initial_v[0])
        models_json[0]["y"]["A"] = int(initial_v[1])
        models_json[0]["y"]["I"] = int(initial_v[2])
        models_json[0]["y"]["R"] = int(initial_v[3])
        models_json[0]["y"]["N"] = int(initial_v[4])

        output.append(models_json[0])

        return output, time

    def get_params_estimation_combine_infected(self, infected, d_op):
        models = read_json(self.params_path)
        return self.build_json_params_metamodel(models, infected, d_op)
