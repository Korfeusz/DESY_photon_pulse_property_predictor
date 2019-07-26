import numpy as np


def get_lowest_non_zero_value(image):
    return np.min(np.nonzero(image))


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


def test_if_point_is_between_two_circles(distance_from_center, r_inner, r_outer):
    if r_inner <= distance_from_center <= r_outer:
        return True
    return False

