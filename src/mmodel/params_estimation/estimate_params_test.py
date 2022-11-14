from mmodel.params_estimation.estimator_class_base import estimator_base
from ..api import ApiConn
from ..json_manager.json_processor import read_json
import numpy as np
from ..constants import GUESS, START_INFECTED
from .calc_params import *


class estimator_test:
    def __init__(self, model_name="model_havana_d29", network_path="", params="", method='diff_evol', iter=6000, numba=False):
        self.opt_func = None
        self.params_path = params
        self.network_path = network_path
        self.model_name = model_name
        self.method = method
        self.iter = iter
        # compiles the model
        self.api = ApiConn(self.model_name, self.network_path, numba)

    def start_sim(self, days, numba):
        self.api.simulate(self.params_path, days, numba)
        return self.__get_ydata__()

    def __get_ydata__(self):
        output = {}
        nodes = self.api.get_network_nodes()
        for node in nodes:
            for c in node.cmodel:
                try:
                    output[c] += self.api.get_ydata_for_node(
                        node.id, c).__next__()
                except KeyError:
                    output[c] = self.api.get_ydata_for_node(
                        node.id, c).__next__()
        return output

    def get_initial_values_SIR_metamodel(self, infected):
        initial_v, guess = self.api.import_params(self.params_path)
        guess = GUESS
        time = len(infected)

        return initial_v, guess, np.linspace(0, time, time)

    def build_json_params_metamodel_combine(self, models_json, acc_infected_by_munc):
        opt_func = estimator_calc_Diff_Evol(self.api, self.iter)

        if self.method == 'pso':
            opt_func = estimator_calc_PSO(self.api, self.iter)
        elif self.method == 'lm':
            opt_func = estimator_calc_LM(self.api, self.iter)

        output = []

        initial_v, guess, time = self.get_initial_values_SIR_metamodel(
            acc_infected_by_munc)

        muncps = [model["label"] for model in models_json]
        params_names = list(models_json[0]["params"].keys())

        new_params, crono = opt_func.estimate_params_metamodel(
            acc_infected_by_munc, time, muncps, initial_v, guess, params_names)

        for i, model in enumerate(models_json):
            model["params"] = new_params[i]
            output.append(model)

        return output, new_params, crono

    def get_params_estimation_combine_infected(self, infected):
        models = read_json(self.params_path)
        return self.build_json_params_metamodel_combine(models, infected)


class estimator_SEAIR(estimator_base):
    def get_initial_values_metamodel(self, models, infected):
        initial_v, guess = self.api.import_params(self.params_path)
        # its where the value of S is in the list for each muncp(order:S,E,A,I,R,N)
        time = -np.inf
        index_N = len(models[0]['model'])
        index_S = models[0]['model'].index('S')

        for model in models:
            infected_by_munc = infected[model["label"]][START_INFECTED:]
            if (len(infected_by_munc) > time):
                time = len(infected_by_munc)

            initial_v[index_S] = initial_v[index_S +
                                           index_N] - infected_by_munc[0]

            index_I = index_S+1

            initial_v[index_I] = infected_by_munc[0]
            # where the initial values of other munc start
            index_S += len(model["y"])

        return initial_v, guess, np.linspace(0, time, time)

    def build_json_params_metamodel(self, models_json, acc_infected_by_munc, d_op):
        output = []
        acc_infected_combine = acc_infected_by_munc
        # d_op.combine_infected_all_mcps(
        #     acc_infected_by_munc)[START_INFECTED:]

        initial_v, guess, time = self.get_initial_values_metamodel(
            models_json, acc_infected_by_munc)

        muncps = [model["label"] for model in models_json]

        params_names = list(models_json[0]["params"].keys())

        new_params, time = self.opt_func.estimate_params_metamodel(
            acc_infected_combine, time, muncps, initial_v, guess, params_names)

        for i, model in enumerate(models_json):
            model["params"] = new_params[i]
            output.append(model)

        return output, time

    def get_params_estimation_combine_infected(self, infected, d_op):
        models = read_json(self.params_path)
        return self.build_json_params_metamodel(models, infected, d_op)
