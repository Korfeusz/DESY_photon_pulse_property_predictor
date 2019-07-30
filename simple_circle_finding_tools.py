import numpy as np
import skimage.measure
import matplotlib.pyplot as plt

def get_distance_from_perfect_circle_greyscale(data, binarisation_levels):
    distance = 0
    for level in binarisation_levels:
        binarised_data = binarise(data, level)
        # plt.imshow(binarised_data[0, :, :])
        # plt.show()
        # print(get_distance_from_perfect_circle_binary(binarised_data))
        distance += get_distance_from_perfect_circle_binary(binarised_data)
    return distance / len(binarisation_levels)

def get_distance_from_perfect_circle_binary(binarised_data):
    perimeters = get_image_perimeters(binarised_data)
    blob_areas = get_blob_areas(binarised_data)
    experimental_ratio = calculate_experimental_circularity_index(perimeters, blob_areas)
    return np.abs(1 - experimental_ratio)


def calculate_experimental_circularity_index(image_perimeters, blob_areas):
    return 4 * np.pi * blob_areas / np.square(image_perimeters)


def get_image_perimeters(data):
    return np.array([skimage.measure.perimeter(image) for image in data])


def get_blob_areas(data):
    return np.sum(np.sum(data != 0, axis=2), axis=1)


def binarise(data, level):
    return (data > level).astype(np.int)


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
    gauss = two_dim_asymmetric_gaussian_function(grid, 10, 0, 0, 20, 20).reshape(size)
    # gauss = gauss +  np.random.random(219*219).reshape((219, 219))
    gauss = gauss.round()
    plt.imshow(gauss)
    plt.show()
    data = np.array([gauss, gauss])


    print(get_distance_from_perfect_circle_greyscale(data, binarisation_levels=(1, 3, 5)))
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