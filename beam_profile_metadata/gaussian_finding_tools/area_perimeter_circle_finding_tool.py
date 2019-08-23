import numpy as np
import skimage.measure
import skimage.filters
from image_manipulation_tools import binarisation_tools


def get_circularity_index(data, binarisation_fractions):
    distance = get_distance_from_perfect_circle_greyscale(data, binarisation_fractions)
    return distance.mean(axis=0)


def get_distance_from_perfect_circle_greyscale(data, binarisation_fractions):
    distance = np.zeros(shape=data.shape[0])
    for fraction in binarisation_fractions:
        binarised_data = binarisation_tools.binarise_by_fraction(data, fraction)
        distance = np.vstack((distance, get_distance_from_perfect_circle_binary(binarised_data)))
    return distance[1:, :]


def get_distance_from_perfect_circle_binary(binarised_data):
    perimeters = get_image_perimeters(binarised_data)
    blob_areas = get_blob_areas(binarised_data)
    experimental_index = calculate_experimental_circularity_index(perimeters, blob_areas)
    return np.abs(1 - experimental_index)


def get_image_perimeters(data):
    return np.array([skimage.measure.perimeter(image) for image in data])


def get_blob_areas(data):
    return np.sum(np.sum(data != 0, axis=2), axis=1)


def calculate_experimental_circularity_index(image_perimeters, blob_areas):
    with np.errstate(divide='ignore', invalid='ignore'):
        return 4 * np.pi * blob_areas / np.square(image_perimeters)


if __name__ == '__main__':
    from beam_profile_metadata.tools import two_dim_asymmetric_gaussian_function
    import matplotlib.pyplot as plt


    def create_grid(image):
        vertical_size, horizontal_size = image.shape
        grid_bound_vertical = vertical_size / 2 - 0.5
        grid_bound_horizontal = horizontal_size / 2 - 0.5
        x = np.linspace(-grid_bound_horizontal, grid_bound_horizontal, horizontal_size)
        y = np.linspace(-grid_bound_vertical, grid_bound_vertical, vertical_size)
        return np.meshgrid(x, y)


    size = (219, 219)
    grid = create_grid(np.zeros(size))
    gauss = two_dim_asymmetric_gaussian_function(grid, 10, 0, 0, 15, 20).reshape(size)
    gauss = gauss.round()
    plt.imshow(gauss)
    plt.show()
    data = np.array([gauss, gauss])
    print(get_circularity_index(data, binarisation_fractions=[0.5, 0.7]))

