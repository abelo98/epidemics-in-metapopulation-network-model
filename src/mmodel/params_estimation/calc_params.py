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
        guess_for_muncps = []

        # builds initial estimations for params*MUNCPS params
        for i in range(len(MUNCPS[:2]) * total_params):
            params_est_name.append(f'param_{i}')
            guess_value = initial_guess["values"][str(i % total_params)]
            guess_for_muncps.append(guess_value)
            params_to_est.add(
                f'param_{i}', value=guess_value, vary=True, min=0, max=1)

        if self.lmfit:
            methods = ['least_squares', 'differential_evolution', 'brute',
                       'basinhopping', 'ampgo', 'nelder', 'lbfgsb', 'powell', 'cg', 'newton', 'cobyla', 'bfgs', 'tnc', 'trust-ncg', 'trust-exact', 'trust-krylov', 'trust-constr', 'dogleg', 'slsqp', 'emcee', 'shgo', 'dual_annealing', 'leastsq']

            for m in methods:
                print(" ")
                print(f'***** {m} *****')
                print(" ")
                fitted_params = minimize(
                    estimator_calc.fit_odeint_metamodel_lmfit, params_to_est, args=(time, ydata,), method=m)

                fitted_params = [
                    fitted_params.params[p].value for p in params_est_name]

                break  # kitar esto
                _ = get_params(initial_guess["names"], muncps, fitted_params)

        else:
            fitted_params, _ = optimize.curve_fit(
                estimator_calc.fit_odeint_metamodel, time, ydata, p0=guess_for_muncps, maxfev=100000)

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
                initial_guess["names"][i], value=initial_guess["values"][str(i)], vary=True, min=0, max=1)

        if self.lmfit:
            fitted_params = minimize(
                estimator_calc.fit_odeint_lmfit, params_to_est, args=(time, ydata,), method='least_squares')

            fitted_params = [
                fitted_params.params[p].value for p in initial_guess["names"]]

        else:
            fitted_params, _ = optimize.curve_fit(
                estimator_calc.fit_odeint, time, ydata, p0=[g for g in initial_guess["values"].values()], maxfev=100000)

        return get_params(initial_guess["names"], [munc], fitted_params)
