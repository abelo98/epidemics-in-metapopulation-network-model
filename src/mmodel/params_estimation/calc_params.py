import numpy as np
from scipy import integrate, optimize
from .params_builder_answer import get_params
from pyswarms.single.global_best import GlobalBestPSO
from .count_time import timer
from .calc_params_base import estimator_calc_base


class estimator_calc_PSO(estimator_calc_base):
    def __init__(self, api, iter):
        global g_api
        g_api = api
        self.iter = iter

    i_values = None
    metamodel = None
    g_api = None

    @staticmethod
    def fit_odeint_metamodel(x, *params):
        if len(params) == 1:
            params = params[0]

        params = np.array(params, dtype=np.float64)

        y_fit = integrate.solve_ivp(
            metamodel.deriv, x, i_values, args=(0.5, 0.1, 0.5, 0.1)).T
        y_infected = g_api.transform_ydata(y_fit)
        return y_infected

    def estimate_params_metamodel(self, ydata: np.array, time: np.array, muncps: list, initial_v, guess, params_names):
        global i_values
        i_values = g_api.transform_input(initial_v)
        i_values = np.array(i_values, dtype=np.float64)

        global metamodel
        metamodel = g_api.import_model(
            g_api.model.name, g_api.model.code_file)

        fitted_params, crono = self.__apply_method__(guess, time, ydata)

        return get_params(params_names, muncps, fitted_params), crono

    @ staticmethod
    def __error_func__(x, time, ydata):
        diff_square = np.zeros(shape=(x.shape[0]), dtype=np.float64)
        for i, particle in enumerate(x):
            infected = estimator_calc_PSO.fit_odeint_metamodel(
                time, particle)

            diff_square[i] = (sum((infected - ydata)**2))/len(ydata)
        return diff_square

    @timer
    def __apply_method__(self, guess, time, ydata):
        x_max = 1 * np.ones(len(guess))
        x_min = 0 * x_max
        particles = 15

        x0 = np.array([guess for _ in range(particles)])
        bounds = (x_min, x_max)
        options = {'c1': 0.5, 'c2': 0.3, 'w': 0.9}
        optimizer = GlobalBestPSO(n_particles=particles, dimensions=len(guess),
                                  options=options, bounds=bounds, init_pos=x0)
        kwargs = {"time": time, "ydata": ydata}
        _, pos = optimizer.optimize(
            self.__error_func__, iters=self.iter, **kwargs)

        return pos


class estimator_calc_LM(estimator_calc_base):
    def __init__(self, api, iter):
        global g_api
        g_api = api
        self.iter = iter

    i_values = None
    metamodel = None
    g_api = None

    @staticmethod
    def fit_odeint_metamodel(x, *params):
        if len(params) == 1:
            params = params[0]

        params = np.array(params, dtype=np.float64)

        y_fit = integrate.odeint(
            metamodel.deriv, i_values, x, args=(params,)).T
        y_infected = g_api.transform_ydata(y_fit)
        return y_infected

    def estimate_params_metamodel(self, ydata: np.array, time: np.array, muncps: list, initial_v, guess, params_names):
        global i_values
        i_values = g_api.transform_input(initial_v)
        i_values = np.array(i_values, dtype=np.float64)

        global metamodel
        metamodel = g_api.import_model(
            g_api.model.name, g_api.model.code_file)

        fitted_params, crono = self.__apply_method__(guess, time, ydata)

        return get_params(params_names, muncps, fitted_params), crono

    @timer
    def __apply_method__(self, guess, time, ydata):
        output, _ = optimize.curve_fit(
            estimator_calc_LM.fit_odeint_metamodel, time, ydata, p0=guess, maxfev=self.iter)
        return output


class estimator_calc_Diff_Evol(estimator_calc_base):
    def __init__(self, api, iter):
        global g_api
        g_api = api
        self.iter = iter

    i_values = None
    metamodel = None
    g_api = None

    @staticmethod
    def fit_odeint_metamodel(x, *params):
        if len(params) == 1:
            params = params[0]

        params = np.array(params, dtype=np.float64)

        y_fit = integrate.solve_ivp(
            metamodel.deriv, x, i_values, args=(params,)).T
        y_infected = g_api.transform_ydata(y_fit)
        return y_infected

    def estimate_params_metamodel(self, ydata: np.array, time: np.array, muncps: list, initial_v, guess, params_names):
        global i_values
        i_values = g_api.transform_input(initial_v)
        i_values = np.array(i_values, dtype=np.float64)

        global metamodel
        metamodel = g_api.import_model(
            g_api.model.name, g_api.model.code_file)

        fitted_params, crono = self.__apply_method__(guess, time, ydata)

        return get_params(params_names, muncps, fitted_params.x), crono

    @ staticmethod
    def __error_func__(x, time, ydata):
        infected = estimator_calc_Diff_Evol.fit_odeint_metamodel(time, x)

        return sum((infected - ydata)**2)/len(ydata)

    @timer
    def __apply_method__(self, guess, time, ydata):
        return optimize.differential_evolution(estimator_calc_Diff_Evol.__error_func__, bounds=[(
            0, 1)]*len(guess), x0=guess, args=(time, ydata), updating='deferred', workers=-1, maxiter=self.iter, popsize=100)
