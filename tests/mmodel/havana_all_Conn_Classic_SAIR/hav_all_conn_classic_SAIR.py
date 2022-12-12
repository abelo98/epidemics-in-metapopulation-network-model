import numpy as np
from scipy.integrate import odeint
def deriv(y, t, params):
	result = np.zeros(shape = (y.size,), dtype=np.float64)
	result[0] =  -(params[0] * ((y[2]) + (y[1])) * y[0]) / ((y[4])) + 1 * y[0] - 1 * y[0]
	result[1] =  (params[0] * ((y[2]) + (y[1])) * y[0]) / ((y[4])) - ((1) / (7)) * y[1] - params[1] * y[1] + 1 * y[1] - 1 * y[1]
	result[2] =  ((1) / (7)) * y[1] - params[1] * y[2] + 1 * y[2] - 1 * y[2]
	result[3] =  params[1] * (y[2] + y[1]) + 1 * y[3] - 1 * y[3]
	result[4] =  0 + 1 * y[4] - 1 * y[4]
	return result


def solve(y, t, params):
	return odeint(deriv, y, t, args=(params,))