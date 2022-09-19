
class SIR:
    @staticmethod
    def sir_ecuations(y, x, beta, gamma):
        S, I, R = y
        dSdt = -beta * S * I / (sum(y))
        dRdt = gamma * I
        dIdt = -(S + R)
        return dSdt, dIdt, dRdt
