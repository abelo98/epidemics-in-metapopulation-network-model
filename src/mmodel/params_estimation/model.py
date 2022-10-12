
from numba import jit


class SIR:

    @staticmethod
    @jit(target_backend='cuda')
    def sir_ecuations(y, x, beta, gamma):
        S, I, R, N = y
        dSdt = -beta * S * I / N
        dRdt = gamma * I
        dIdt = -(dSdt + dRdt)
        dNdt = 0
        return dSdt, dIdt, dRdt, dNdt
