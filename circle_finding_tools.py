import numpy as np


def get_lowest_non_zero_values(data):
    return np.nanmin(np.nanmin(np.where(data == 0, np.nan, data), axis=2), axis=1)


def calculate_expected_ratio_inside_ribbon_to_entire_disk(r_inner, r_outer, r_total):
    return (np.power(r_outer, 2) - np.power(r_inner, 2)) / np.power(r_total, 2)


def create_grid(image):
    vertical_size, horizontal_size = image.shape
    grid_bound_vertical = vertical_size / 2 - 0.5
    grid_bound_horizontal = horizontal_size / 2 - 0.5
    x = np.linspace(-grid_bound_horizontal, grid_bound_horizontal, horizontal_size)
    y = np.linspace(-grid_bound_vertical, grid_bound_vertical, vertical_size)
    return np.meshgrid(x, y)


def create_matrix_of_distances_from_center(image):
    x, y = create_grid(image)
    return np.linalg.norm(np.dstack((x, y)), axis=2)


def create_ring_mask(r_inner, r_outer, distance_matrix):
    return (distance_matrix < r_outer) & (distance_matrix > r_inner)


def count_all_non_zero_points(data):
    return np.sum(np.sum(data != 0, axis=2), axis=1)


def count_non_zero_points_under_mask(data, masks):
    return np.sum(np.sum((data != 0) & masks, axis=2), axis=1)
