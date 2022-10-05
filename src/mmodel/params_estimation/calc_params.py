from ..json_manager.json_processor import read_json
import numpy as np
from scipy import integrate, optimize
from .model import SIR
from ..constants import MUNCPS
from lmfit import Parameters, minimize
from .params_builder_answer import get_params


class estimator_calc:
    def __init__(self, guess_path, params_path, api, lmfit=False):
        self.guess_path = guess_path
        self.params_path = params_path
        self.api = api
        self.lmfit = lmfit
        # self.params_path = "tests/mmodel/simple/params/simple_params.json"

    i_values = None
    metamodel = None

    @ staticmethod
    def fit_odeint(x, beta, gamma):
        return integrate.odeint(SIR.sir_ecuations, i_values, x, args=(beta, gamma))[:, 1]

    @ staticmethod
    def fit_odeint_metamodel(x, *params):
        return integrate.odeint(metamodel.deriv, i_values, x, args=(params,))[:, 1]

    @ staticmethod
    def fit_odeint_lmfit(params, x, y):
        beta = params["beta"]
        gamma = params["gamma"]
        y_fit = integrate.odeint(
            SIR.sir_ecuations, i_values, x, args=(beta, gamma))[:, 1]
        return y_fit - y

    @ staticmethod
    def fit_odeint_metamodel_lmfit(params, x, y):
        params = [p for p in params.values()]
        y_fit = integrate.odeint(
            metamodel.deriv, i_values, x, args=(params,))[:, 1]
        return y_fit - y

    def estimate_params_metamodel(self, ydata: np.array, time: np.array, muncps: list, id=0):
        # imports and expand for mncps initial values
        global i_values
        i_values, _ = self.api.import_params(self.params_path)
        i_values = self.api.transform_input(i_values)

        # imports the metamodel
        global metamodel
        metamodel = self.api.import_model(
            self.api.model.name, self.api.model.code_file)

        # reads params initial guess json
        initial_guess = read_json(self.guess_path)
        total_params = len(initial_guess)

        params_to_est = Parameters()
        params_est_name = []

        # builds initial estimations for params*MUNCPS params
        for i in range(len(MUNCPS) * total_params):
            params_est_name.append(f'guess_{i}')
            params_to_est.add(
                f'guess_{i}', value=initial_guess["values"][str(i % total_params)], vary=True)

        if self.lmfit:
            fitted_params = minimize(
                estimator_calc.fit_odeint_metamodel_lmfit, params_to_est, args=(time, ydata,), method='least_squares')

            fitted_params = [
                fitted_params.params[p].value for p in initial_guess["names"]]

        else:
            fitted_params, _ = optimize.curve_fit(
                estimator_calc.fit_odeint_metamodel, time, ydata, p0=[g for g in initial_guess["values"].values()], maxfev=5000)

        return get_params(initial_guess["names"], muncps, fitted_params, id)

    def estimate_params_single_model(self, ydata: np.array, time: np.array, initial_v: dict, munc):
        global i_values
        i_values = tuple(initial_v.values())

        fitted_params = None

        params_to_est = Parameters()

        # reads params initial guess json
        initial_guess = read_json(self.guess_path)
        total_params = len(initial_guess)

        for i in range(total_params):
            params_to_est.add(
                initial_guess["names"][i], value=initial_guess["values"][str(i)], vary=True)

        if self.lmfit:
            fitted_params = minimize(
                estimator_calc.fit_odeint_lmfit, params_to_est, args=(time, ydata,), method='least_squares')

            fitted_params = [
                fitted_params.params[p].value for p in initial_guess["names"]]

        else:
            fitted_params, _ = optimize.curve_fit(
                estimator_calc.fit_odeint, time, ydata, p0=[g for g in initial_guess["values"].values()], maxfev=5000)

        return get_params(initial_guess["names"], [munc], fitted_params)
