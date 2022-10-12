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
        try:
            y_fit = integrate.odeint(
                metamodel.deriv, i_values, x, args=(params,)).T
            y_infected = g_api.transform_ydata(y_fit)
        except:
            print("error")
        return y_infected

    @ staticmethod
    def fit_odeint_lmfit(params, x, y):
        beta = params["beta"]
        gamma = params["gamma"]
        y_fit = integrate.odeint(
            SIR.sir_ecuations, i_values, x, args=(beta, gamma))[:, 1]
        # y_infected = g_api.transform_ydata(y_fit)
        return y_fit - y

    @ staticmethod
    def fit_odeint_metamodel_lmfit(params, x, y):
        params = [p for p in params.values()]
        y_fit = metamodel.solve(y, x, params).T
        y_infected = g_api.transform_ydata(y_fit)

        return y_infected - y

    def estimate_params_metamodel(self, ydata: np.array, time: np.array, muncps: list, initial_v, initial_guess, params_names, id=0):
        # imports and expand for mncps initial values
        global i_values
        # i_values, _ = self.api.import_params(self.params_path)
        i_values = self.api.transform_input(initial_v)

        # imports the metamodel
        global metamodel
        metamodel = self.api.import_model(
            self.api.model.name, self.api.model.code_file)

        # reads params initial guess json
        # initial_guess = read_json(self.guess_path)
        total_params = len(initial_guess)

        params_to_est = Parameters()
        params_est_name = []
        # guess_for_muncps = []

        if self.lmfit:
            # builds initial estimations for params*MUNCPS params
            for i in range(len(MUNCPS) * total_params):
                params_est_name.append(f'param_{i}')
                guess_value = initial_guess[i % total_params]
                params_to_est.add(
                    f'param_{i}', value=guess_value, vary=True, min=0, max=1)
            # methods = ['least_squares', 'differential_evolution', 'brute',
            #            'basinhopping', 'ampgo', 'nelder', 'lbfgsb', 'powell', 'cobyla', 'bfgs', 'tnc', 'slsqp', 'shgo', 'dual_annealing', 'leastsq']

            # for m in methods:
            # print(" ")
            # print(f'***** {m} *****')
            # print(" ")
            fitted_params = minimize(
                estimator_calc.fit_odeint_metamodel_lmfit, params_to_est, args=(time, ydata,), max_nfev=1000)

            fitted_params = [
                fitted_params.params[p].value for p in params_est_name]

            # break  # kitar esto
            # _ = get_params(initial_guess["names"], muncps, fitted_params)

        else:
            fitted_params, _ = optimize.curve_fit(
                estimator_calc.fit_odeint_metamodel, time, ydata, p0=initial_guess, bounds=(0, 1), check_finite=True, maxfev=1000)

        return get_params(params_names, muncps, fitted_params, id)

    def estimate_params_single_model(self, ydata: np.array, time: np.array, initial_v: dict, initial_guess, params_names, munc):
        global i_values
        i_values = tuple(initial_v.values())

        fitted_params = None

        # reads params initial guess json
        # initial_guess = read_json(self.guess_path)
        total_params = len(initial_guess)

        if self.lmfit:
            params_to_est = Parameters()

            for i in range(total_params):
                params_to_est.add(
                    params_names[i], value=initial_guess[i], vary=True, min=0, max=1)

            fitted_params = minimize(
                estimator_calc.fit_odeint_lmfit, params_to_est, args=(time, ydata,), method='least_squares')

            fitted_params = [
                fitted_params.params[p].value for p in params_names]

        else:
            fitted_params, _ = optimize.curve_fit(
                estimator_calc.fit_odeint, time, ydata, p0=initial_guess, maxfev=100000)

        return get_params(params_names, [munc], fitted_params)
