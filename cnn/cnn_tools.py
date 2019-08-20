import numpy as np


def lr_decay(epoch):
    # return 0.01 * np.power(0.666, epoch)
    return 0.01 * np.power(0.95, epoch)

