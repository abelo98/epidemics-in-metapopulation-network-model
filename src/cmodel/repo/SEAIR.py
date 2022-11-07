from scipy.integrate import odeint


class SEAIR:

    sets = ['S', 'E', 'A', 'I', 'R']
    params = ['gamma', 'beta', 'alpha', 'N']
    equations = {
        'S': lambda S, E, A, I, R, _S, _E, _A, _I, _R, gamma, beta, alpha, N: f' -({beta} * ({I} + {A}) * {S}) / ({N})',
        'E': lambda S, E, A, I, R, _S, _E, _A, _I, _R, gamma, beta, alpha, N: f' ({beta} * ({I} + {A}) * {S}) / ({N}) - {alpha} * {E}',
        'A': lambda S, E, A, I, R, _S, _E, _A, _I, _R, gamma, beta, alpha, N: f' (1 - (1) / (7)) * {alpha} * {E} - {gamma} * {A}',
        'I': lambda S, E, A, I, R, _S, _E, _A, _I, _R, gamma, beta, alpha, N: f' ((1) / (7)) * {alpha} * {E} - {gamma} * {I}',
        'R': lambda S, E, A, I, R, _S, _E, _A, _I, _R, gamma, beta, alpha, N: f' {gamma} * ({I} + {A})',
    }

    @staticmethod
    def deriv(y, t, params):
        S, E, A, I, R = y
        gamma, beta, alpha, N = params
        dSdt = -(beta * (I + A) * S) / (N)
        dEdt = (beta * (I + A) * S) / (N) - alpha * E
        dAdt = (1 - (1) / (7)) * alpha * E - gamma * A
        dIdt = ((1) / (7)) * alpha * E - gamma * I
        dRdt = gamma * (I + A)
        return dSdt, dEdt, dAdt, dIdt, dRdt

    @staticmethod
    def solve(y, t, params):
        return odeint(SEAIR.deriv, y, t, args=(params,))
