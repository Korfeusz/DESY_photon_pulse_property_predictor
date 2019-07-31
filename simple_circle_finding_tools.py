import numpy as np
import skimage.measure, skimage.filters
import matplotlib.pyplot as plt
from binarisation_tools import binarise_by_fraction

def get_position_of_most_circular_images(circularity_indeces, number_of_best):
    best_positions_unsorted = np.argpartition(circularity_indeces, number_of_best)[:number_of_best]
    best_values_sorted_indeces = np.argsort(circularity_indeces[best_positions_unsorted])
    return best_positions_unsorted[best_values_sorted_indeces]


def get_circularity_index(data, binarisation_fractions):
    distance = get_distance_from_perfect_circle_greyscale(data, binarisation_fractions)
    return distance.mean(axis=0)


def get_distance_from_perfect_circle_greyscale(data, binarisation_fractions):
    distance = np.zeros(shape=data.shape[0])
    for fraction in binarisation_fractions:
        binarised_data = binarise_by_fraction(data, fraction)
        # plt.imshow(binarised_data[90, :, :])
        # plt.show()
        distance = np.vstack((distance, get_distance_from_perfect_circle_binary(binarised_data)))
    return distance[1:, :]


def get_distance_from_perfect_circle_binary(binarised_data):
    perimeters = get_image_perimeters(binarised_data)
    blob_areas = get_blob_areas(binarised_data)
    experimental_index = calculate_experimental_circularity_index(perimeters, blob_areas)
    return np.abs(1 - experimental_index)


def calculate_experimental_circularity_index(image_perimeters, blob_areas):
    with np.errstate(divide='ignore', invalid='ignore'):
        return 4 * np.pi * blob_areas / np.square(image_perimeters)


def get_image_perimeters(data):
    return np.array([skimage.measure.perimeter(image) for image in data])


def get_blob_areas(data):
    return np.sum(np.sum(data != 0, axis=2), axis=1)





if __name__ == '__main__':
    from gaussian_fit_tools import two_dim_symmetric_gaussian_function, two_dim_asymmetric_gaussian_function
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
    # gauss = gauss +  np.random.random(219*219).reshape((219, 219))
    gauss = gauss.round()
    plt.imshow(gauss)
    plt.show()
    data = np.array([gauss, gauss])


    # print(get_distance_from_perfect_circle_greyscale(data, binarisation_levels=[2]))
    # label_image = skimage.measure.label(data[0, :, :])
    # regions = regionprops = skimage.measure.regionprops(label_image)
    # fig, ax = plt.subplots()
    # ax.imshow(data[0, :, :], cmap=plt.cm.gray)
    #
    # for props in regions:
    #     minr, minc, maxr, maxc = props.bbox
    #     bx = (minc, maxc, maxc, minc, minc)
    #     by = (minr, minr, maxr, maxr, minr)
    #     ax.plot(bx, by, '-b', linewidth=2.5)
    #
    #     print((props.area / np.square(props.perimeter)) * 4 * np.pi)
    # plt.show()

    # thr = skimage.filters.threshold_otsu(data)
    # print(thr)
    # plt.imshow(binarise(data, thr)[0, :, :])
    # plt.show()


    print(get_circularity_index(data, binarisation_fractions=[0.5, 0.7]))

    a = np.array([1, 9, 2, 8, 3, 8, 3, 6, 5, 7, 3, 78, 5, 2, 563, 23])
    print(get_position_of_most_circular_images(a, 4))
    print(a[get_position_of_most_circular_images(a, 4)])
