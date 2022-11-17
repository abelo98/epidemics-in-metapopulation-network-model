from scipy.integrate import odeint


class SAIR:

    sets = ['S', 'A', 'I', 'R', 'N']
    params = ['gamma', 'beta']
    equations = {
        'S': lambda S, A, I, R, N, _S, _A, _I, _R, _N, gamma, beta: f' -({beta} * ({I} + {A}) * {S}) / ({_N})',
        'A': lambda S, A, I, R, N, _S, _A, _I, _R, _N, gamma, beta: f' ({beta} * ({I} + {A}) * {S}) / ({_N}) - ((1) / (7)) * {A} - {gamma} * {A}',
        'I': lambda S, A, I, R, N, _S, _A, _I, _R, _N, gamma, beta: f' ((1) / (7)) * {A} - {gamma} * {I}',
        'R': lambda S, A, I, R, N, _S, _A, _I, _R, _N, gamma, beta: f' {gamma} * ({I} + {A})',
        'N': lambda S, A, I, R, N, _S, _A, _I, _R, _N, gamma, beta: f' 0',
    }

    @staticmethod
    def deriv(y, t, params):
        S, A, I, R, N = y
        gamma, beta = params
        dSdt = -(beta * (I + A) * S) / (N)
        dAdt = (beta * (I + A) * S) / (N) - ((1) / (7)) * A - gamma * A
        dIdt = ((1) / (7)) * A - gamma * I
        dRdt = gamma * (I + A)
        dNdt = 0
        return dSdt, dAdt, dIdt, dRdt, dNdt

    @staticmethod
    def solve(y, t, params):
        return odeint(SAIR.deriv, y, t, args=(params,))
