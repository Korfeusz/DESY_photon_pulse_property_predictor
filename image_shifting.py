import numpy as np


def shift_left(image, value):
    return np.pad(image, ((0, 0), (0, value)), mode='constant')[:, value:]


def shift_right(image, value):
    return np.pad(image, ((0, 0), (value, 0)), mode='constant')[:, :-value]


def shift_up(image, value):
    return np.pad(image, ((0, value), (0, 0)), mode='constant')[value:, :]


def shift_down(image, value):
    return np.pad(image, ((value, 0), (0, 0)), mode='constant')[:-value, :]


def shift_image(image, horizontal, vertical):
    if horizontal > 0:
        image = shift_right(image, horizontal)
    else:
        image = shift_left(image, -horizontal)
    if vertical > 0:
        image = shift_up(image, vertical)
    else:
        image = shift_down(image, -vertical)
    return image

