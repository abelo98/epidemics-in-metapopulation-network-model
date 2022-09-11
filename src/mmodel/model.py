from scipy import integrate

class SIR:
    def __init__(self,initial_v:dict) -> None:
        self.S0 = initial_v['S']
        self.I0 = initial_v['I']
        self.R0 = initial_v['R']
        self.N = initial_v['N']
        
    def sir_ecuations(self,y, x, beta, gamma):
        S = -beta * y[0] * y[1] / self.N
        R = gamma * y[1]
        I = -(S + R)
        return S, I, R


    def fit_odeint(self,x, beta, gamma):
        return integrate.odeint(self.sir_model, (self.S0, self.I0, self.R0), x, args=(beta, gamma))[:, 1]
