import numba as nb
import numpy as np
from scipy import integrate, optimize
from .model import SIR
from .params_builder_answer import get_params
from pyswarms.single.global_best import GlobalBestPSO
import time


class estimator_calc:
    def __init__(self, api, method='diff_evol', iter=6000):
        global g_api
        g_api = api
        self.api = api
        self.method = method
        self.iter = iter

    i_values = None
    metamodel = None
    g_api = None

    def timer(f):
        def wrapper_timer(*args, **kargs):
            start = time.time()
            output = f(*args, **kargs)
            stop = time.time()
            crono = stop-start
            # print(" ")
            # print(f'elapsed time: {crono}')
            # print(" ")
            return output, crono
        return wrapper_timer

    @ staticmethod
    def fit_odeint(x, beta, gamma):
        y_fit = integrate.odeint(
            SIR.sir_ecuations, i_values, x, args=(beta, gamma))[:, 1]
        return y_fit

    @ staticmethod
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
        i_values = self.api.transform_input(initial_v)

        global metamodel
        metamodel = self.api.import_model(
            self.api.model.name, self.api.model.code_file)

        if self.method == 'pso':
            fitted_params, crono = self.apply_pso(guess, time, ydata)
        elif self.method == 'curve_fit':
            fitted_params, crono = self.apply_curve_fit(guess, time, ydata)
        else:
            fitted_params, crono = self.apply_optimization_func(
                guess, time, ydata)
            fitted_params = fitted_params.x

        return get_params(params_names, muncps, fitted_params), crono

    def estimate_params_single_model(self, ydata: np.array, time: np.array, initial_v: dict, initial_guess, params_names, munc):
        global i_values
        i_values = tuple(initial_v.values())

        fitted_params, _ = optimize.curve_fit(
            estimator_calc.fit_odeint, time, ydata, p0=initial_guess, maxfev=100000)

        return get_params(params_names, [munc], fitted_params)

    @ staticmethod
    def __mse_for_pso__(x, time, ydata):
        diff_square = np.zeros(shape=(x.shape[0]), dtype=np.float64)
        for i, particle in enumerate(x):
            infected = estimator_calc.fit_odeint_metamodel(
                time, particle)

            diff_square[i] = (sum((infected - ydata)**2)/len(ydata))
        return diff_square

    @ staticmethod
    def __mse__(x, time, ydata):
        infected = estimator_calc.fit_odeint_metamodel(
            time, x)

        return sum((infected - ydata)**2)/len(ydata)

    @timer
    def apply_pso(self, guess, time, ydata):
        x_max = 1 * np.ones(len(guess))
        x_min = 0 * x_max
        particles = 6

        x0 = np.array([guess for _ in range(particles)])
        bounds = (x_min, x_max)
        options = {'c1': 0.5, 'c2': 0.3, 'w': 0.9}
        optimizer = GlobalBestPSO(n_particles=particles, dimensions=len(guess),
                                  options=options, bounds=bounds, init_pos=x0)
        kwargs = {"time": time, "ydata": ydata}
        _, pos = optimizer.optimize(
            estimator_calc.__mse_for_pso__, iters=self.iter, n_processes=6, **kwargs)

        return pos

    @timer
    def apply_curve_fit(self, guess, time, ydata):
        output, _ = optimize.curve_fit(
            estimator_calc.fit_odeint_metamodel, time, ydata, p0=guess, bounds=(0, 1), maxfev=self.iter)
        return output

    @timer
    def apply_optimization_func(self, guess, time, ydata):
        return optimize.differential_evolution(estimator_calc.__mse__, bounds=[(
            0, 1)]*len(guess), x0=guess, args=(time, ydata), updating='deferred', workers=-1, maxiter=self.iter)
