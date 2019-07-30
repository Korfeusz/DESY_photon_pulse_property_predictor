import numpy as np


def get_circularity_area_perimeter_index(data):
    perimeters = get_image_perimeters(data)
    blob_areas = get_blob_areas(data)
    experimental_ratio = calculate_experimental_perimeter_square_area_ratio(perimeters, blob_areas)
    return np.abs(4 * np.pi - experimental_ratio)


def calculate_experimental_perimeter_square_area_ratio(image_perimeters, blob_areas):
    return np.square(image_perimeters) / blob_areas


def get_image_perimeters(data):
    pass


def get_blob_areas(data):
    pass



