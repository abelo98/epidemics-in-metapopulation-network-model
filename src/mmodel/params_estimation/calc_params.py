import numpy as np
from scipy import integrate, optimize
from .model import SIR
from ..constants import MUNCPS
from lmfit import Parameters, minimize
from .params_builder_answer import get_params
from pyswarms.single.global_best import GlobalBestPSO


class estimator_calc:
    def __init__(self, guess_path, params_path, api, lmfit=False):
        self.guess_path = guess_path
        self.params_path = params_path
        global g_api
        g_api = api
        self.api = api
        self.lmfit = lmfit
        # self.params_path = "tests/mmodel/simple/params/simple_params.json"

    i_values = None
    metamodel = None
    g_api = None

    @ staticmethod
    def fit_odeint(x, beta, gamma):
        y_fit = integrate.odeint(
            SIR.sir_ecuations, i_values, x, args=(beta, gamma))[:, 1]
        return y_fit

    @ staticmethod
    def fit_odeint_metamodel(x, *params):
        y_fit = integrate.odeint(
            metamodel.deriv, i_values, x, args=(params,)).T
        y_infected = g_api.transform_ydata(y_fit)
        return y_infected

    def estimate_params_metamodel(self, ydata: np.array, time: np.array, muncps: list, initial_v, initial_guess, params_names, id=0):
        # imports and expand for mncps initial values
        global i_values
        # i_values, _ = self.api.import_params(self.params_path)
        i_values = self.api.transform_input(initial_v)

        # imports the metamodel
        global metamodel
        metamodel = self.api.import_model(
            self.api.model.name, self.api.model.code_file)

        fitted_params, _ = optimize.curve_fit(
            estimator_calc.fit_odeint_metamodel, time, ydata, p0=initial_guess, bounds=(0, 1), maxfev=5000)

        return get_params(params_names, muncps, fitted_params, id)

    def estimate_params_single_model(self, ydata: np.array, time: np.array, initial_v: dict, initial_guess, params_names, munc):
        global i_values
        i_values = tuple(initial_v.values())

        fitted_params, _ = optimize.curve_fit(
            estimator_calc.fit_odeint, time, ydata, p0=initial_guess, maxfev=100000)

        return get_params(params_names, [munc], fitted_params)

    @ staticmethod
    def mse(x, time, ydata):
        infected = estimator_calc.fit_odeint_metamodel(
            time, x[0, :])

        diff_square = sum((infected - ydata)**2)/len(ydata)
        return diff_square

    def pso(self, guess, time, ydata):
        x_max = 1 * np.ones(len(guess))
        x_min = 0 * x_max

        bounds = (x_min, x_max)
        options = {'c1': 0.5, 'c2': 0.3, 'w': 0.9}
        optimizer = GlobalBestPSO(n_particles=1, dimensions=4,
                                  options=options, bounds=bounds)

        kwargs = {"time": time, "ydata": ydata}
        _, pos = optimizer.optimize(estimator_calc.mse, 1000, **kwargs)

        return pos
