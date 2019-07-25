import numpy as np
import scipy.ndimage


def shift_left(image, value):
    return np.pad(image, ((0, 0), (0, value)), mode='constant')[:, value:]


def shift_right(image, value):
    return np.pad(image, ((0, 0), (value, 0)), mode='constant')[:, :-value]


def shift_up(image, value):
    return np.pad(image, ((0, value), (0, 0)), mode='constant')[value:, :]


def shift_down(image, value):
    return np.pad(image, ((value, 0), (0, 0)), mode='constant')[:-value, :]


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


def get_geometric_center(image):
    return np.round([x/2 for x in image.shape]).astype(np.int)


def get_center_of_mass(image):
    if np.count_nonzero(image) == 0:
        return get_geometric_center(image)
    return np.array(scipy.ndimage.measurements.center_of_mass(image)).astype(np.int)


def get_shift_values(image):
    y_center_of_mass, x_center_of_mass = get_center_of_mass(image)
    y_geometric, x_geometric = get_geometric_center(image)
    return x_geometric - x_center_of_mass, -(y_geometric - y_center_of_mass)


def shift_com_to_geometric_single_image(image):
    horizontal, vertical = get_shift_values(image)
    return shift_by_values(image, horizontal=horizontal, vertical=vertical)


def shift_com_to_geometric(data):
    return np.array(list(map(shift_com_to_geometric_single_image, data)))

