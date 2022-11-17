from scipy.integrate import odeint


class SAIR:

    sets = ['S', 'A', 'I', 'R', 'N']
    params = ['beta', 'gamma']
    equations = {
        'S': lambda S, A, I, R, N, _S, _A, _I, _R, _N, beta, gamma: f' -({beta} * ({_I} + {_A}) * {S}) / ({_N})',
        'A': lambda S, A, I, R, N, _S, _A, _I, _R, _N, beta, gamma: f' ({beta} * ({_I} + {_A}) * {S}) / ({_N}) - ((1) / (7)) * {A} - {gamma} * {A}',
        'I': lambda S, A, I, R, N, _S, _A, _I, _R, _N, beta, gamma: f' ((1) / (7)) * {A} - {gamma} * {I}',
        'R': lambda S, A, I, R, N, _S, _A, _I, _R, _N, beta, gamma: f' {gamma} * ({I} + {A})',
        'N': lambda S, A, I, R, N, _S, _A, _I, _R, _N, beta, gamma: f' 0',
    }

    @staticmethod
    def deriv(y, t, params):
        S, A, I, R, N = y
        beta, gamma = params
        dSdt = -(beta * (I + A) * S) / (N)
        dAdt = (beta * (I + A) * S) / (N) - ((1) / (7)) * A - gamma * A
        dIdt = ((1) / (7)) * A - gamma * I
        dRdt = gamma * (I + A)
        dNdt = 0
        return dSdt, dAdt, dIdt, dRdt, dNdt

    @staticmethod
    def solve(y, t, params):
        return odeint(SAIR.deriv, y, t, args=(params,))
