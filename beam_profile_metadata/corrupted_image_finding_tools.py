import numpy as np


def find_empty_images(data, threshold=0):
    return [False if s > threshold else True for s in np.sum(np.sum(data, axis=2), axis=1)]
