import numpy as np


def binarise_by_fraction(data, fraction):
    maxvals = get_max_values_per_image(data)
    thresholds = get_thresholds(fraction, maxvals)
    return binarise_by_level(data, broadcast_thresholds_to_image_shape(thresholds,  data.shape[-2:]))


def binarise_by_level(data, broadcast_thresholds):
    return (data > broadcast_thresholds)


def get_max_values_per_image(data):
    return data.max(axis=2).max(axis=1)


def get_thresholds(fraction, maxvals):
    return fraction * maxvals


def broadcast_thresholds_to_image_shape(levels, image_shape):
    return np.tensordot(levels, np.ones(image_shape), axes=0)
