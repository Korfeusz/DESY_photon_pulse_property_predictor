import numpy as np
from skimage import morphology
import binarisation_tools

def change_color_resolution(data, new_resolution, old_resolution):
    return data / old_resolution * new_resolution


def get_flattened_shape(data):
    shape = data.shape
    return shape[0], shape[1] * shape[2]


def get_nth_lowest_vals(data, n=2):
    flat_shape = get_flattened_shape(data)
    array_of_unique_values = np.array(list(map(np.unique, np.reshape(data, flat_shape))))
    return [x[n-1] if len(x) > n else min(x) for x in array_of_unique_values]


def create_mask_from_lowest_vals(data, nth_lowest_values):
    flat_shape = get_flattened_shape(data)
    return np.reshape([x <= y for x, y in zip(np.reshape(data, flat_shape), nth_lowest_values)], data.shape)


def put_zeros_under_mask(data, mask):
    data[mask] = 0.
    return data


def convert_values_to_initial_resolution(values, initial_color_resolution, processing_color_resolution):
    return np.array(values) / processing_color_resolution * initial_color_resolution


def subtract_background(data, converted_highest_background_values):
    flat_shape = get_flattened_shape(data)
    return np.reshape([x - y for x, y in zip(np.reshape(data, flat_shape), converted_highest_background_values)],
                      data.shape)


def grayscale_opening(data):
    return np.array(list(map(morphology.opening, data)))


def remove_background(data, initial_color_resolution, processing_color_resolution, number_of_lowest_to_cut=2):
    mask = change_color_resolution(data=data,
                                   new_resolution=processing_color_resolution,
                                   old_resolution=initial_color_resolution)
    mask = np.round(mask)
    nth_lowest_values = get_nth_lowest_vals(mask, n=number_of_lowest_to_cut)
    mask = create_mask_from_lowest_vals(mask, nth_lowest_values=nth_lowest_values)
    converted_highest_background_values = convert_values_to_initial_resolution(nth_lowest_values,
                                                                               initial_color_resolution,
                                                                               processing_color_resolution)
    data = subtract_background(data, converted_highest_background_values=converted_highest_background_values)
    data = put_zeros_under_mask(data, mask)
    return data


def alternative_remove_background(data, intensity_fraction):
    maxvals = binarisation_tools.get_max_values_per_image(data)
    thresholds = binarisation_tools.get_thresholds(intensity_fraction, maxvals)

    broadcast_thresholds = binarisation_tools.broadcast_thresholds_to_image_shape(thresholds, data.shape[-2:])
    mask = binarisation_tools.binarise_by_level(data, broadcast_thresholds)
    data = data - broadcast_thresholds
    data[~mask] = 0.
    return data