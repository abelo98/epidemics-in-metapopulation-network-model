from numba import njit
import numpy as np
from scipy.integrate import odeint


@njit
def deriv(y, t, params):
	result = np.zeros(shape = (len(y),), dtype=np.float64)
	result[0] =  -(params[0] * y[0] * (y[4]+y[6])) / ((y[12]+y[14])) + 0.5 * y[1] - 0.5 * y[0]
	result[1] =  -(params[2] * y[1] * (y[5]+y[7])) / ((y[13]+y[15])) + 0.5 * y[0] - 0.5 * y[1]
	result[2] =  -(params[0] * y[2] * (y[4]+y[6])) / ((y[12]+y[14])) + 0.5 * y[3] - 0.5 * y[2]
	result[3] =  -(params[2] * y[3] * (y[5]+y[7])) / ((y[13]+y[15])) + 0.5 * y[2] - 0.5 * y[3]
	result[4] =  (params[0] * y[0] * (y[4]+y[6])) / ((y[12]+y[14])) - params[1] * y[4] + 0.5 * y[5] - 0.5 * y[4]
	result[5] =  (params[2] * y[1] * (y[5]+y[7])) / ((y[13]+y[15])) - params[3] * y[5] + 0.5 * y[4] - 0.5 * y[5]
	result[6] =  (params[0] * y[2] * (y[4]+y[6])) / ((y[12]+y[14])) - params[1] * y[6] + 0.5 * y[7] - 0.5 * y[6]
	result[7] =  (params[2] * y[3] * (y[5]+y[7])) / ((y[13]+y[15])) - params[3] * y[7] + 0.5 * y[6] - 0.5 * y[7]
	result[8] =  params[1] * y[4] + 0.5 * y[9] - 0.5 * y[8]
	result[9] =  params[3] * y[5] + 0.5 * y[8] - 0.5 * y[9]
	result[10] =  params[1] * y[6] + 0.5 * y[11] - 0.5 * y[10]
	result[11] =  params[3] * y[7] + 0.5 * y[10] - 0.5 * y[11]
	result[12] =  0 + 0.5 * y[13] - 0.5 * y[12]
	result[13] =  0 + 0.5 * y[12] - 0.5 * y[13]
	result[14] =  0 + 0.5 * y[15] - 0.5 * y[14]
	result[15] =  0 + 0.5 * y[14] - 0.5 * y[15]
	return result


def solve(y, t, params):
	return odeint(deriv, y, t, args=(params,))