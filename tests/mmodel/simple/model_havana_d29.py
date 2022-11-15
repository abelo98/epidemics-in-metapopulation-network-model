import numpy as np
from scipy.integrate import odeint
from numba import njit, jit, cuda


@njit
def deriv(y, t, params):
	result = np.zeros(shape = (y.size,), dtype=np.float64)
	result[0] =  -(params[2] * (y[12] + y[8]) * y[0]) / ((y[20]+y[22])) + 0.5 * y[1] - 0.5 * y[0]
	result[1] =  -(params[5] * (y[13] + y[9]) * y[1]) / ((y[21]+y[23])) + 0.5 * y[0] - 0.5 * y[1]
	result[2] =  -(params[2] * (y[14] + y[10]) * y[2]) / ((y[20]+y[22])) + 0.5 * y[3] - 0.5 * y[2]
	result[3] =  -(params[5] * (y[15] + y[11]) * y[3]) / ((y[21]+y[23])) + 0.5 * y[2] - 0.5 * y[3]
	result[4] =  (params[2] * (y[12] + y[8]) * y[0]) / ((y[20]+y[22])) - params[0] * y[4] + 0.5 * y[5] - 0.5 * y[4]
	result[5] =  (params[5] * (y[13] + y[9]) * y[1]) / ((y[21]+y[23])) - params[3] * y[5] + 0.5 * y[4] - 0.5 * y[5]
	result[6] =  (params[2] * (y[14] + y[10]) * y[2]) / ((y[20]+y[22])) - params[0] * y[6] + 0.5 * y[7] - 0.5 * y[6]
	result[7] =  (params[5] * (y[15] + y[11]) * y[3]) / ((y[21]+y[23])) - params[3] * y[7] + 0.5 * y[6] - 0.5 * y[7]
	result[8] =  (1 - (1) / (7)) * params[0] * y[4] - params[1] * y[8] + 0.5 * y[9] - 0.5 * y[8]
	result[9] =  (1 - (1) / (7)) * params[3] * y[5] - params[4] * y[9] + 0.5 * y[8] - 0.5 * y[9]
	result[10] =  (1 - (1) / (7)) * params[0] * y[6] - params[1] * y[10] + 0.5 * y[11] - 0.5 * y[10]
	result[11] =  (1 - (1) / (7)) * params[3] * y[7] - params[4] * y[11] + 0.5 * y[10] - 0.5 * y[11]
	result[12] =  ((1) / (7)) * params[0] * y[4] - params[1] * y[12] + 0.5 * y[13] - 0.5 * y[12]
	result[13] =  ((1) / (7)) * params[3] * y[5] - params[4] * y[13] + 0.5 * y[12] - 0.5 * y[13]
	result[14] =  ((1) / (7)) * params[0] * y[6] - params[1] * y[14] + 0.5 * y[15] - 0.5 * y[14]
	result[15] =  ((1) / (7)) * params[3] * y[7] - params[4] * y[15] + 0.5 * y[14] - 0.5 * y[15]
	result[16] =  params[1] * (y[12] + y[8]) + 0.5 * y[17] - 0.5 * y[16]
	result[17] =  params[4] * (y[13] + y[9]) + 0.5 * y[16] - 0.5 * y[17]
	result[18] =  params[1] * (y[14] + y[10]) + 0.5 * y[19] - 0.5 * y[18]
	result[19] =  params[4] * (y[15] + y[11]) + 0.5 * y[18] - 0.5 * y[19]
	result[20] =  0 + 0.5 * y[21] - 0.5 * y[20]
	result[21] =  0 + 0.5 * y[20] - 0.5 * y[21]
	result[22] =  0 + 0.5 * y[23] - 0.5 * y[22]
	result[23] =  0 + 0.5 * y[22] - 0.5 * y[23]
	return result


def solve(y, t, params):
	return odeint(deriv, y, t, args=(params,))