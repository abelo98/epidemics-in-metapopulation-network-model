from scipy.integrate import odeint


class SEAIR:

    sets = ['S', 'E', 'A', 'I', 'R', 'N']
    params = ['alpha', 'gamma', 'beta']
    equations = {
        'S': lambda S, E, A, I, R, N, _S, _E, _A, _I, _R, _N, alpha, gamma, beta: f' -({beta} * ({I} + {A}) * {S}) / ({_N})',
        'E': lambda S, E, A, I, R, N, _S, _E, _A, _I, _R, _N, alpha, gamma, beta: f' ({beta} * ({I} + {A}) * {S}) / ({_N}) - {alpha} * {E}',
        'A': lambda S, E, A, I, R, N, _S, _E, _A, _I, _R, _N, alpha, gamma, beta: f'  ((1) / (7)) * {alpha} * {E} - {gamma} * {A}',
        'I': lambda S, E, A, I, R, N, _S, _E, _A, _I, _R, _N, alpha, gamma, beta: f' (1 - (1) / (7)) * {alpha} * {E} - {gamma} * {I}',
        'R': lambda S, E, A, I, R, N, _S, _E, _A, _I, _R, _N, alpha, gamma, beta: f' {gamma} * ({I} + {A})',
        'N': lambda S, E, A, I, R, N, _S, _E, _A, _I, _R, _N, alpha, gamma, beta: f' 0',
    }

    @staticmethod
    def deriv(y, t, params):
        S, E, A, I, R, N = y
        alpha, gamma, beta = params
        dSdt = -(beta * (I + A) * S) / (N)
        dEdt = (beta * (I + A) * S) / (N) - alpha * E
        dAdt = (0.8571) * alpha * E - gamma * A
        dIdt = (0.1428) * alpha * E - gamma * I
        dRdt = gamma * (I + A)
        dNdt = 0
        return dSdt, dEdt, dAdt, dIdt, dRdt, dNdt

    @staticmethod
    def solve(y, t, params):
        return odeint(SEAIR.deriv, y, t, args=(params,))
