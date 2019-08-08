import numpy as np
import scipy.ndimage
import skimage.measure

from image_manipulation_tools import binarisation_tools


def shift_com_to_geometric(data):
    return np.array(list(map(shift_com_to_geometric_single_image, data)))


def shift_com_to_geometric_single_image(image):
    horizontal, vertical = get_shift_to_com_values(image)
    return shift_by_values(image, horizontal=horizontal, vertical=vertical)


def get_shift_to_com_values(image):
    y_center_of_mass, x_center_of_mass = get_center_of_mass(image)
    y_geometric, x_geometric = get_geometric_center(image)
    return x_geometric - x_center_of_mass, -(y_geometric - y_center_of_mass)


def get_center_of_mass(image):
    if np.count_nonzero(image) == 0:
        return get_geometric_center(image)
    return np.array(scipy.ndimage.measurements.center_of_mass(image)).astype(np.int)


def shift_highest_intensity_to_geometric(data, fraction):
    binarised_data = binarisation_tools.binarise_by_fraction(data, fraction)
    new_data = np.zeros(shape=data.shape)
    for i, image in enumerate(binarised_data):
        label_image = skimage.measure.label(image)
        regions = skimage.measure.regionprops(label_image)
        if regions:
            areas = [prop.area for prop in regions]
            centers = [[x.astype(np.int) for x in prop.centroid] for prop in regions]
            max_index = np.argmax(areas)
            peak_center = centers[max_index]
            geom_center = get_geometric_center(data[0, :, :])
            horizontal, vertical = get_shift_values(geom_center, peak_center)
            shifted_image = shift_by_values(data[i, :, :], horizontal, vertical)
        else:
            shifted_image = data[i, :, :]
        new_data[i, :, :] = shifted_image
    return new_data


def get_geometric_center(image):
    return np.round([x / 2 for x in image.shape]).astype(np.int)


def get_shift_values(geometric_center, new_center):
    y_geo, x_geo = geometric_center
    y_new, x_new = new_center
    return x_geo - x_new, -(y_geo - y_new)


def shift_by_values(image, horizontal, vertical):
    if np.abs(horizontal) > image.shape[1]:
        horizontal = np.sign(horizontal) * image.shape[1]
    if np.abs(vertical) > image.shape[0]:
        vertical = np.sign(vertical) * image.shape[0]
    if horizontal > 0:
        image = shift_right(image, horizontal)
    elif horizontal < 0:
        image = shift_left(image, -horizontal)
    if vertical > 0:
        image = shift_up(image, vertical)
    elif vertical < 0:
        image = shift_down(image, -vertical)
    return image


def shift_left(image, value):
    return np.pad(image, ((0, 0), (0, value)), mode='constant')[:, value:]


def shift_right(image, value):
    return np.pad(image, ((0, 0), (value, 0)), mode='constant')[:, :-value]


def shift_up(image, value):
    return np.pad(image, ((0, value), (0, 0)), mode='constant')[value:, :]


def shift_down(image, value):
    return np.pad(image, ((value, 0), (0, 0)), mode='constant')[:-value, :]


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
    gauss_1 = two_dim_asymmetric_gaussian_function(grid, 10, 5, 7, 15, 23).reshape(size)
    gauss_2 = two_dim_asymmetric_gaussian_function(grid, 10, -20, -50, 20, 15).reshape(size)
    gauss = gauss_1 + gauss_2
    gauss = gauss.round()
    plt.imshow(gauss)
    plt.show()
    data = np.array([gauss, gauss])

    dat = shift_highest_intensity_to_geometric(data, fraction=0.9)

    plt.imshow(dat[0, :, :])
    plt.show()
