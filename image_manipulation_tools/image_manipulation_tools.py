import numpy as np
from skimage import morphology
from image_manipulation_tools import binarisation_tools


def change_color_resolution(data, new_resolution, old_resolution):
    return data / old_resolution * new_resolution


def grayscale_opening(data):
    return np.array(list(map(morphology.opening, data)))


def remove_background_by_intensity_fraction(data, intensity_fraction):
    maxvals = binarisation_tools.get_max_values_per_image(data)
    thresholds = binarisation_tools.get_thresholds(intensity_fraction, maxvals)

    broadcast_thresholds = binarisation_tools.broadcast_thresholds_to_image_shape(thresholds, data.shape[-2:])
    mask = binarisation_tools.binarise_by_level(data, broadcast_thresholds)
    data = data - broadcast_thresholds
    data[~mask] = 0.
    return data