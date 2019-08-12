import numpy as np

def one_hot(data, num_classes):
    length = data.shape[0]
    one_hot = np.zeros((length, num_classes))
    one_hot[np.arange(length), data] = 1
    return one_hot

