from functools import reduce

import numpy as np


def reshape_codes(codes):
    new_code_shape = reduce(lambda x, y: x * y, codes.shape[1:])
    return np.reshape(codes, newshape=(codes.shape[0], new_code_shape))