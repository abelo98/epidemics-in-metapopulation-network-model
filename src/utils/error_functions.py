import numpy as np


def mse(params_est, real_params):
    output = sum((params_est - real_params)**2)/len(real_params)
    return output
