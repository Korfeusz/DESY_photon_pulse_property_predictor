import numpy as np


def is_circle_in_center_of_images(data, ring_thickness=5, number_of_tests=2):
    r_total = get_mask_radii(data)
    r_outer = r_total
    circularity_index = 0
    for test_no in range(number_of_tests):
        r_outer = r_outer - (test_no) * ring_thickness
        r_inner = r_outer - ring_thickness
        experimental_ratio, expected_ratio = get_ribbon_ratios(data, r_outer, r_inner, r_total)
        circularity_index += get_circularity_index(experimental_ratio, expected_ratio)
    circularity_index /= number_of_tests
    return circularity_index


def get_mask_radii(data):
    return np.sqrt(count_all_non_zero_points(data) / np.pi)


def count_all_non_zero_points(data):
    return np.sum(np.sum(data != 0, axis=2), axis=1)


def get_ribbon_ratios(data, r_outer, r_inner, r_total):
    experimental_ratio = calculate_experimental_ratio_inside_ribbon_to_entire_disk(data, r_inner, r_outer)
    expected_ratio = calculate_expected_ratio_inside_ribbon_to_entire_disk(r_inner, r_outer, r_total)
    return experimental_ratio, expected_ratio


def calculate_experimental_ratio_inside_ribbon_to_entire_disk(data, r_inner, r_outer):
    dist_mat = create_matrix_of_distances_from_center(data[0, :, :])
    ring_masks = create_ring_mask(r_inner, r_outer, dist_mat)
    with np.errstate(divide='ignore', invalid='ignore'):
        return count_non_zero_points_under_mask(data, ring_masks) / count_all_non_zero_points(data)


def count_non_zero_points_under_mask(data, masks):
    return np.sum(np.sum((data != 0) & masks, axis=2), axis=1)


def create_matrix_of_distances_from_center(image):
    x, y = create_grid(image)
    return np.linalg.norm(np.dstack((x, y)), axis=2)


def create_grid(image):
    vertical_size, horizontal_size = image.shape
    grid_bound_vertical = vertical_size / 2 - 0.5
    grid_bound_horizontal = horizontal_size / 2 - 0.5
    x = np.linspace(-grid_bound_horizontal, grid_bound_horizontal, horizontal_size)
    y = np.linspace(-grid_bound_vertical, grid_bound_vertical, vertical_size)
    return np.meshgrid(x, y)


def create_ring_mask(r_inner, r_outer, distance_matrix):
    r_inner_matrix = broadcast_radii_to_data_shape(r_inner, distance_matrix.shape)
    r_outer_matrix = broadcast_radii_to_data_shape(r_outer, distance_matrix.shape)
    return (distance_matrix < r_outer_matrix) & (distance_matrix > r_inner_matrix)


def broadcast_radii_to_data_shape(radii, image_shape):
    return np.tensordot(radii, np.ones(image_shape), axes=0)


def calculate_expected_ratio_inside_ribbon_to_entire_disk(r_inner, r_outer, r_total):
    with np.errstate(divide='ignore', invalid='ignore'):
        return (np.square(r_outer) - np.square(r_inner)) / np.square(r_total)


def get_circularity_index(experimental_ratio, expected_ratio):
    return np.abs(1 - np.abs(experimental_ratio / expected_ratio))


if __name__ == '__main__':
    from beam_profile_metadata.tools import two_dim_asymmetric_gaussian_function
    import matplotlib.pyplot as plt

    grid = create_grid(np.zeros((219, 219)))
    gauss = two_dim_asymmetric_gaussian_function(grid, 10, 0, 0, 18, 20).reshape((219, 219))
    gauss = gauss.round()
    plt.imshow(gauss)
    plt.show()
    data = np.array([gauss, gauss])
    val = is_circle_in_center_of_images(data, ring_thickness=5, number_of_tests=4)
    print(val)
