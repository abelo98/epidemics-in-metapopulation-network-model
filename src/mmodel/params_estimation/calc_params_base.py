import numpy as np


class estimator_calc_base:
    def __init__(self, method: str, iter=6000):
        self.method = method
        self.iter = iter

    @ staticmethod
    def fit_odeint_metamodel(x, *params):
        raise NotImplementedError()

    def estimate_params_metamodel(self, ydata: np.array, time: np.array, muncps: list, initial_v, guess, params_names):
        raise NotImplementedError()

    @ staticmethod
    def __error_func__(x, time, ydata):
        raise NotImplementedError()

    def __apply_method__(self, guess, time, ydata):
        raise NotImplementedError()
