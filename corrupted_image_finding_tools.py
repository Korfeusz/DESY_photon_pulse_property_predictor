import numpy as np


def find_empty_images(data):
    return [False if s != 0 else True for s in np.sum(np.sum(data, axis=2), axis=1)]
