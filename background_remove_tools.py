import numpy as np
import beam_profile_imaging


def change_color_resolution(data, new_resolution, old_resolution):
    return data / old_resolution * new_resolution


def get_flattened_shape(data):
    shape = data.shape
    return shape[0], shape[1] * shape[2]


def get_nth_lowest_vals(data, n=2):
    flat_shape = get_flattened_shape(data)
    return [x[n-1] for x in np.array(list(map(np.unique, np.reshape(data, flat_shape))))]


def create_mask_from_lowest_vals(data, nth_lowest_values):
    flat_shape = get_flattened_shape(data)
    return np.reshape([x <= y for x, y in zip(np.reshape(data, flat_shape), nth_lowest_values)], data.shape)


def put_zeros_under_mask(data, mask):
    data[mask] = 0.
    return data


def subtract_background(data, highest_background_value):
    flat_shape = get_flattened_shape(data)
    return np.reshape([x - y for x, y in zip(np.reshape(data, flat_shape), highest_background_value)], data.shape)


def remove_background(data, initial_color_resolution, processing_color_resolution, number_of_lowest_to_cut=2):
    mask = change_color_resolution(data=data,
                                   new_resolution=processing_color_resolution,
                                   old_resolution=initial_color_resolution)
    mask = np.round(mask)
    beam_profile_imaging.save_beam_profile_image(mask[1, :, :], name='bckgrnd.png')
    nth_lowest_values = get_nth_lowest_vals(mask, n=number_of_lowest_to_cut)
    print(nth_lowest_values)
    mask = create_mask_from_lowest_vals(mask, nth_lowest_values=nth_lowest_values)
    data = put_zeros_under_mask(data, mask)
    data = subtract_background(data, highest_background_value=nth_lowest_values)
    return data
