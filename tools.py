import numpy as np


def get_n_highest_values(circularity_indeces, number_of_best):
    best_positions_unsorted = np.argpartition(circularity_indeces, number_of_best)[:number_of_best]
    best_values_sorted_indeces = np.argsort(circularity_indeces[best_positions_unsorted])
    return best_positions_unsorted[best_values_sorted_indeces]


def two_dim_asymmetric_gaussian_function(grid, amplitude, mu_x, mu_y, sigma_x, sigma_y):
    x, y = grid
    mu_x = float(mu_x)
    mu_y = float(mu_y)
    gaussian = amplitude * np.exp(-(((x - mu_x) ** 2) / (2 * sigma_x ** 2) + ((y - mu_y) ** 2) / (2 * sigma_y ** 2)))
    return gaussian.ravel()
