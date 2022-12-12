import numpy as np
import math as mt


def mse(params_est, real_params):
    output = mt.sqrt(sum((params_est - real_params)**2)/len(real_params))
    return round(output, 4)
