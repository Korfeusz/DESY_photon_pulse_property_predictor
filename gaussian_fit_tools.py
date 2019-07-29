import numpy as np
import scipy.optimize as opt


def two_dim_symmetric_gaussian_function(grid, amplitude, mu_x, mu_y, sigma):
    x, y = grid
    mu_x = float(mu_x)
    mu_y = float(mu_y)
    gaussian = amplitude * np.exp(-(((x - mu_x) ** 2) / (2 * sigma ** 2) + ((y - mu_y) ** 2) / (2 * sigma ** 2)))
    return gaussian.ravel()

def get_initial_guess(image):
    pass

import numpy as np
import scipy.optimize as opt
import gaussian_fit_tools


class GaussianPipeline:
    def __init__(self, data):
        self.data = data
        self.shape = data.shape
        self.grid = self.create_grid()

    def get_image_shape(self):
        return self.shape[-2:]

    def create_grid(self):
        vertical_size, horizontal_size = self.get_image_shape()
        grid_bound_vertical = vertical_size / 2 - 0.5
        grid_bound_horizontal = horizontal_size / 2 - 0.5
        x = np.linspace(-grid_bound_horizontal, grid_bound_horizontal, horizontal_size)
        y = np.linspace(-grid_bound_vertical, grid_bound_vertical, vertical_size)
        return np.meshgrid(x, y)

    def fit_gaussian(self):

        popt, pcov = opt.curve_fit(gaussian_fit_tools.two_dim_symmetric_gaussian_function,
                                   self.grid,
                                   self.data,
                                   p0=gaussian_fit_tools.get_initial_guess)