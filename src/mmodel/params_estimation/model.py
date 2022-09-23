from scipy.integrate import odeint


class SIR:
    @staticmethod
    def sir_ecuations(y, x, beta, gamma):
        S, I, R, N = y
        dSdt = -beta * S * I / N
        dRdt = gamma * I
        dIdt = -(S + R)
        dNdt = 0
        return dSdt, dIdt, dRdt, dNdt
