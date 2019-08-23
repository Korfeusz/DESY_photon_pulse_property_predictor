import numpy as np


def one_hot(data, num_classes):
    length = data.shape[0]
    one_ho = np.zeros((length, num_classes))
    one_ho[np.arange(length), data] = 1
    return one_ho

