from scipy import integrate


class SIR:
    def __init__(self, initial_v: dict) -> None:
        self.S0 = initial_v['S']
        self.I0 = initial_v['I']
        self.R0 = initial_v['R']
        self.N = initial_v['N']

    @staticmethod
    def sir_ecuations(y, x, beta, gamma):
        S = -beta * y[0] * y[1] / (sum(y))
        R = gamma * y[1]
        I = -(S + R)
        return S, I, R


