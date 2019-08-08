import numpy as np


def get_indices_of_n_lowest_values(array_of_values, number_to_find):
    best_positions_unsorted = np.argpartition(array_of_values, number_to_find)[:number_to_find]
    best_values_sorted_indices = np.argsort(array_of_values[best_positions_unsorted])
    return best_positions_unsorted[best_values_sorted_indices]


def get_indices_of_n_highest_values(array_of_values, number_to_find):
    worst_positions_unsorted = np.argpartition(array_of_values, -number_to_find)[-number_to_find:]
    worst_values_sorted_indices = np.argsort(array_of_values[worst_positions_unsorted])
    return worst_positions_unsorted[worst_values_sorted_indices]


def two_dim_asymmetric_gaussian_function(grid, amplitude, mu_x, mu_y, sigma_x, sigma_y):
    x, y = grid
    mu_x = float(mu_x)
    mu_y = float(mu_y)
    gaussian = amplitude * np.exp(-(((x - mu_x) ** 2) / (2 * sigma_x ** 2) + ((y - mu_y) ** 2) / (2 * sigma_y ** 2)))
    return gaussian.ravel()
