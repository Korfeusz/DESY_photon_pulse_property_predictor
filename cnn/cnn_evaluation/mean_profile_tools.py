import numpy as np
from scipy.optimize import curve_fit
import matplotlib.pyplot as plt


def get_profiles_labeled_1(predictions, data):
    return data[predictions, :, :]

def get_profiles_labeled_0(predictions, data):
    return data[~predictions, :, :]

def create_mean_profile(data):
    return np.mean(data, axis=0)


def two_dim_asymmetric_gaussian_function(grid, amplitude, mu_x, mu_y, sigma_x, sigma_y):
    x, y = grid
    mu_x = float(mu_x)
    mu_y = float(mu_y)
    gaussian = amplitude * np.exp(-(((x - mu_x) ** 2) / (2 * sigma_x ** 2) + ((y - mu_y) ** 2) / (2 * sigma_y ** 2)))
    return gaussian.ravel()


def fit_gaussian_to_profile(profile):
    y_shape, x_shape = profile.shape
    x = np.linspace(-int(x_shape / 2), int(x_shape / 2), x_shape)
    y = np.linspace(-int(y_shape / 2), int(y_shape / 2), y_shape)
    (x, y) = np.meshgrid(x, y)

    p0 = 1500, 0, 0, 20, 20
    popt, pcov = curve_fit(two_dim_asymmetric_gaussian_function, (x, y), profile.ravel(), p0=p0)
    data_fitted = two_dim_asymmetric_gaussian_function((x, y), *popt)

    fig, ax = plt.subplots(1, 1)
    ax.imshow(profile, cmap=plt.cm.jet, origin='lower',
              extent=(x.min(), x.max(), y.min(), y.max()))
    ax.contour(x, y, data_fitted.reshape(y_shape, x_shape), 8, colors='w')

    plt.show()
    fit = {
        'Amplitude': popt[0],
        'X_mean': popt[1],
        'Y_mean': popt[2],
        'sigma_x': popt[3],
        'sigma_y': popt[4]
    }
    return fit
