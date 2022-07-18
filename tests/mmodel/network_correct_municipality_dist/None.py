from scipy.integrate import odeint


def deriv(y, t, params):
	result = [0] * len(y)
	result[0] =  -(params[0] * y[0] * y[1]) / (y[3]) + 0.3 * y[56] + 0.8 * y[52] + 0.7 * y[44] + 0.5 * y[40] + 0.5 * y[0] - 2.3 * y[0]
	result[1] =  (params[0] * y[0] * y[1]) / (y[3]) - params[1] * y[1] + 0.3 * y[57] + 0.8 * y[53] + 0.7 * y[45] + 0.5 * y[41] + 0.5 * y[1] - 2.3 * y[1]
	result[2] =  params[1] * y[1] + 0.3 * y[58] + 0.8 * y[54] + 0.7 * y[46] + 0.5 * y[42] + 0.5 * y[2] - 2.3 * y[2]
	result[3] =  0 + 0.3 * y[59] + 0.8 * y[55] + 0.7 * y[47] + 0.5 * y[43] + 0.5 * y[3] - 2.3 * y[3]
	result[4] =  -(params[2] * y[4] * y[5]) / (y[7]) + 0.5 * y[8] + 0.5 * y[12] + 0.5 * y[16] + 0.5 * y[4] - 2.0 * y[4]
	result[5] =  (params[2] * y[4] * y[5]) / (y[7]) - params[3] * y[5] + 0.5 * y[9] + 0.5 * y[13] + 0.5 * y[17] + 0.5 * y[5] - 2.0 * y[5]
	result[6] =  params[3] * y[5] + 0.5 * y[10] + 0.5 * y[14] + 0.5 * y[18] + 0.5 * y[6] - 2.0 * y[6]
	result[7] =  0 + 0.5 * y[11] + 0.5 * y[15] + 0.5 * y[19] + 0.5 * y[7] - 2.0 * y[7]
	result[8] =  -(params[4] * y[8] * y[9]) / (y[11]) + 0.1 * y[28] + 0.5 * y[32] + 0.5 * y[4] + 0.5 * y[12] + 0.5 * y[8] - 2.5 * y[8]
	result[9] =  (params[4] * y[8] * y[9]) / (y[11]) - params[5] * y[9] + 0.1 * y[29] + 0.5 * y[33] + 0.5 * y[5] + 0.5 * y[13] + 0.5 * y[9] - 2.5 * y[9]
	result[10] =  params[5] * y[9] + 0.1 * y[30] + 0.5 * y[34] + 0.5 * y[6] + 0.5 * y[14] + 0.5 * y[10] - 2.5 * y[10]
	result[11] =  0 + 0.1 * y[31] + 0.5 * y[35] + 0.5 * y[7] + 0.5 * y[15] + 0.5 * y[11] - 2.5 * y[11]
	result[12] =  -(params[6] * y[12] * y[13]) / (y[15]) + 0.5 * y[0] + 0.5 * y[28] + 0.5 * y[32] + 0.5 * y[8] + 0.5 * y[4] + 0.5 * y[16] + 0.5 * y[12] - 3.0 * y[12]
	result[13] =  (params[6] * y[12] * y[13]) / (y[15]) - params[7] * y[13] + 0.5 * y[1] + 0.5 * y[29] + 0.5 * y[33] + 0.5 * y[9] + 0.5 * y[5] + 0.5 * y[17] + 0.5 * y[13] - 3.0 * y[13]
	result[14] =  params[7] * y[13] + 0.5 * y[2] + 0.5 * y[30] + 0.5 * y[34] + 0.5 * y[10] + 0.5 * y[6] + 0.5 * y[18] + 0.5 * y[14] - 3.0 * y[14]
	result[15] =  0 + 0.5 * y[3] + 0.5 * y[31] + 0.5 * y[35] + 0.5 * y[11] + 0.5 * y[7] + 0.5 * y[19] + 0.5 * y[15] - 3.0 * y[15]
	result[16] =  -(params[8] * y[16] * y[17]) / (y[19]) + 0.3 * y[20] + 0.6 * y[24] + 0.5 * y[28] + 0.5 * y[4] + 0.5 * y[12] + 0.5 * y[16] - 3.0 * y[16]
	result[17] =  (params[8] * y[16] * y[17]) / (y[19]) - params[9] * y[17] + 0.3 * y[21] + 0.6 * y[25] + 0.5 * y[29] + 0.5 * y[5] + 0.5 * y[13] + 0.5 * y[17] - 3.0 * y[17]
	result[18] =  params[9] * y[17] + 0.3 * y[22] + 0.6 * y[26] + 0.5 * y[30] + 0.5 * y[6] + 0.5 * y[14] + 0.5 * y[18] - 3.0 * y[18]
	result[19] =  0 + 0.3 * y[23] + 0.6 * y[27] + 0.5 * y[31] + 0.5 * y[7] + 0.5 * y[15] + 0.5 * y[19] - 3.0 * y[19]
	result[20] =  -(params[10] * y[20] * y[21]) / (y[23]) + 0.2 * y[48] + 0.1 * y[44] + 0.5 * y[24] + 0.1 * y[28] + 0.5 * y[16] + 0.5 * y[20] - 2.1 * y[20]
	result[21] =  (params[10] * y[20] * y[21]) / (y[23]) - params[11] * y[21] + 0.2 * y[49] + 0.1 * y[45] + 0.5 * y[25] + 0.1 * y[29] + 0.5 * y[17] + 0.5 * y[21] - 2.1 * y[21]
	result[22] =  params[11] * y[21] + 0.2 * y[50] + 0.1 * y[46] + 0.5 * y[26] + 0.1 * y[30] + 0.5 * y[18] + 0.5 * y[22] - 2.1 * y[22]
	result[23] =  0 + 0.2 * y[51] + 0.1 * y[47] + 0.5 * y[27] + 0.1 * y[31] + 0.5 * y[19] + 0.5 * y[23] - 2.1 * y[23]
	result[24] =  -(params[12] * y[24] * y[25]) / (y[27]) + 0.5 * y[44] + 0.5 * y[20] + 0.1 * y[40] + 0.5 * y[28] + 0.5 * y[16] + 0.5 * y[24] - 3.3000000000000003 * y[24]
	result[25] =  (params[12] * y[24] * y[25]) / (y[27]) - params[13] * y[25] + 0.5 * y[45] + 0.5 * y[21] + 0.1 * y[41] + 0.5 * y[29] + 0.5 * y[17] + 0.5 * y[25] - 3.3000000000000003 * y[25]
	result[26] =  params[13] * y[25] + 0.5 * y[46] + 0.5 * y[22] + 0.1 * y[42] + 0.5 * y[30] + 0.5 * y[18] + 0.5 * y[26] - 3.3000000000000003 * y[26]
	result[27] =  0 + 0.5 * y[47] + 0.5 * y[23] + 0.1 * y[43] + 0.5 * y[31] + 0.5 * y[19] + 0.5 * y[27] - 3.3000000000000003 * y[27]
	result[28] =  -(params[14] * y[28] * y[29]) / (y[31]) + 0.2 * y[20] + 0.5 * y[24] + 0.5 * y[40] + 0.1 * y[36] + 0.5 * y[32] + 0.5 * y[8] + 0.5 * y[12] + 0.5 * y[16] + 0.5 * y[28] - 3.7 * y[28]
	result[29] =  (params[14] * y[28] * y[29]) / (y[31]) - params[15] * y[29] + 0.2 * y[21] + 0.5 * y[25] + 0.5 * y[41] + 0.1 * y[37] + 0.5 * y[33] + 0.5 * y[9] + 0.5 * y[13] + 0.5 * y[17] + 0.5 * y[29] - 3.7 * y[29]
	result[30] =  params[15] * y[29] + 0.2 * y[22] + 0.5 * y[26] + 0.5 * y[42] + 0.1 * y[38] + 0.5 * y[34] + 0.5 * y[10] + 0.5 * y[14] + 0.5 * y[18] + 0.5 * y[30] - 3.7 * y[30]
	result[31] =  0 + 0.2 * y[23] + 0.5 * y[27] + 0.5 * y[43] + 0.1 * y[39] + 0.5 * y[35] + 0.5 * y[11] + 0.5 * y[15] + 0.5 * y[19] + 0.5 * y[31] - 3.7 * y[31]
	result[32] =  -(params[16] * y[32] * y[33]) / (y[35]) + 0.5 * y[36] + 0.5 * y[28] + 0.5 * y[8] + 0.5 * y[12] + 0.5 * y[32] - 2.5 * y[32]
	result[33] =  (params[16] * y[32] * y[33]) / (y[35]) - params[17] * y[33] + 0.5 * y[37] + 0.5 * y[29] + 0.5 * y[9] + 0.5 * y[13] + 0.5 * y[33] - 2.5 * y[33]
	result[34] =  params[17] * y[33] + 0.5 * y[38] + 0.5 * y[30] + 0.5 * y[10] + 0.5 * y[14] + 0.5 * y[34] - 2.5 * y[34]
	result[35] =  0 + 0.5 * y[39] + 0.5 * y[31] + 0.5 * y[11] + 0.5 * y[15] + 0.5 * y[35] - 2.5 * y[35]
	result[36] =  -(params[18] * y[36] * y[37]) / (y[39]) + 0.2 * y[40] + 0.5 * y[28] + 0.5 * y[32] + 0.5 * y[36] - 1.2 * y[36]
	result[37] =  (params[18] * y[36] * y[37]) / (y[39]) - params[19] * y[37] + 0.2 * y[41] + 0.5 * y[29] + 0.5 * y[33] + 0.5 * y[37] - 1.2 * y[37]
	result[38] =  params[19] * y[37] + 0.2 * y[42] + 0.5 * y[30] + 0.5 * y[34] + 0.5 * y[38] - 1.2 * y[38]
	result[39] =  0 + 0.2 * y[43] + 0.5 * y[31] + 0.5 * y[35] + 0.5 * y[39] - 1.2 * y[39]
	result[40] =  -(params[20] * y[40] * y[41]) / (y[43]) + 0.6 * y[44] + 0.6 * y[24] + 0.1 * y[36] + 0.5 * y[28] + 0.5 * y[40] - 2.3 * y[40]
	result[41] =  (params[20] * y[40] * y[41]) / (y[43]) - params[21] * y[41] + 0.6 * y[45] + 0.6 * y[25] + 0.1 * y[37] + 0.5 * y[29] + 0.5 * y[41] - 2.3 * y[41]
	result[42] =  params[21] * y[41] + 0.6 * y[46] + 0.6 * y[26] + 0.1 * y[38] + 0.5 * y[30] + 0.5 * y[42] - 2.3 * y[42]
	result[43] =  0 + 0.6 * y[47] + 0.6 * y[27] + 0.1 * y[39] + 0.5 * y[31] + 0.5 * y[43] - 2.3 * y[43]
	result[44] =  -(params[22] * y[44] * y[45]) / (y[47]) + 0.2 * y[0] + 0.7 * y[52] + 0.5 * y[48] + 0.1 * y[20] + 0.5 * y[20] + 0.6 * y[24] + 0.5 * y[40] + 0.5 * y[44] - 3.5000000000000004 * y[44]
	result[45] =  (params[22] * y[44] * y[45]) / (y[47]) - params[23] * y[45] + 0.2 * y[1] + 0.7 * y[53] + 0.5 * y[49] + 0.1 * y[21] + 0.5 * y[21] + 0.6 * y[25] + 0.5 * y[41] + 0.5 * y[45] - 3.5000000000000004 * y[45]
	result[46] =  params[23] * y[45] + 0.2 * y[2] + 0.7 * y[54] + 0.5 * y[50] + 0.1 * y[22] + 0.5 * y[22] + 0.6 * y[26] + 0.5 * y[42] + 0.5 * y[46] - 3.5000000000000004 * y[46]
	result[47] =  0 + 0.2 * y[3] + 0.7 * y[55] + 0.5 * y[51] + 0.1 * y[23] + 0.5 * y[23] + 0.6 * y[27] + 0.5 * y[43] + 0.5 * y[47] - 3.5000000000000004 * y[47]
	result[48] =  -(params[24] * y[48] * y[49]) / (y[51]) + 0.6 * y[52] + 0.5 * y[44] + 0.5 * y[48] - 2.0 * y[48]
	result[49] =  (params[24] * y[48] * y[49]) / (y[51]) - params[25] * y[49] + 0.6 * y[53] + 0.5 * y[45] + 0.5 * y[49] - 2.0 * y[49]
	result[50] =  params[25] * y[49] + 0.6 * y[54] + 0.5 * y[46] + 0.5 * y[50] - 2.0 * y[50]
	result[51] =  0 + 0.6 * y[55] + 0.5 * y[47] + 0.5 * y[51] - 2.0 * y[51]
	result[52] =  -(params[26] * y[52] * y[53]) / (y[55]) + 0.6 * y[0] + 0.6 * y[56] + 0.8 * y[48] + 0.1 * y[44] + 0.5 * y[52] - 3.1 * y[52]
	result[53] =  (params[26] * y[52] * y[53]) / (y[55]) - params[27] * y[53] + 0.6 * y[1] + 0.6 * y[57] + 0.8 * y[49] + 0.1 * y[45] + 0.5 * y[53] - 3.1 * y[53]
	result[54] =  params[27] * y[53] + 0.6 * y[2] + 0.6 * y[58] + 0.8 * y[50] + 0.1 * y[46] + 0.5 * y[54] - 3.1 * y[54]
	result[55] =  0 + 0.6 * y[3] + 0.6 * y[59] + 0.8 * y[51] + 0.1 * y[47] + 0.5 * y[55] - 3.1 * y[55]
	result[56] =  -(params[28] * y[56] * y[57]) / (y[59]) + 0.5 * y[0] + 0.5 * y[52] + 0.5 * y[44] + 0.5 * y[56] - 1.4 * y[56]
	result[57] =  (params[28] * y[56] * y[57]) / (y[59]) - params[29] * y[57] + 0.5 * y[1] + 0.5 * y[53] + 0.5 * y[45] + 0.5 * y[57] - 1.4 * y[57]
	result[58] =  params[29] * y[57] + 0.5 * y[2] + 0.5 * y[54] + 0.5 * y[46] + 0.5 * y[58] - 1.4 * y[58]
	result[59] =  0 + 0.5 * y[3] + 0.5 * y[55] + 0.5 * y[47] + 0.5 * y[59] - 1.4 * y[59]
	return result


def solve(y, t, params):
	return odeint(deriv, y, t, args=(params,))