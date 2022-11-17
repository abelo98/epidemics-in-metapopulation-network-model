from ..json_manager.json_processor import read_json
import numpy as np
from ..constants import START_INFECTED
from .estimator_class_base import estimator_base


class estimator_SIR_classic(estimator_base):
    def get_initial_values_metamodel(self, models, infected_all_comb):
        initial_v, guess = self.api.import_params(self.params_path)
        # its where the value of S is in the list for each muncp(order:S,I,R,N)
        time = -np.inf
        index_N = len(models[0]['model'])
        index_S = models[0]['model'].index('S')

        initial_v[index_S] = initial_v[index_S + index_N] - \
            infected_all_comb[START_INFECTED]

        index_I = index_S+1

        initial_v[index_I] = infected_all_comb[START_INFECTED]

        return initial_v, guess, np.linspace(0, time, time)

    def build_json_params_metamodel(self, models_json, acc_infected_by_munc, d_op):
        output = []
        acc_infected_combine = d_op.combine_infected_all_mcps(
            acc_infected_by_munc)

        initial_v, guess, time = self.get_initial_values_metamodel(
            models_json, acc_infected_combine)

        muncps = [model["label"] for model in models_json]

        params_names = list(models_json[0]["params"].keys())
        acc_infected_combine = acc_infected_combine[START_INFECTED:]

        new_params, time = self.opt_func.estimate_params_metamodel(
            acc_infected_combine, time, muncps, initial_v, guess, params_names)

        for i, model in enumerate(models_json):
            model["params"] = new_params[i]
            output.append(model)

        return output, time

    def get_params_estimation_combine_infected(self, infected, d_op):
        models = read_json(self.params_path)
        return self.build_json_params_metamodel(models, infected, d_op)
