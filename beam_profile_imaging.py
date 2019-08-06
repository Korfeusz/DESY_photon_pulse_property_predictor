import matplotlib.pyplot as plt
import numpy as np
import json_tools
import beam_profile_metadata_tools
import beam_profiles_import_tool


def save_beam_profile_image(beam_profile, name='save_test.png'):
    plt.imsave(name,
               beam_profile,
               cmap=plt.cm.jet)


def show_beam_profile(beam_profiles, image_number):
    plt.imshow(beam_profiles[image_number, :, :], cmap=plt.cm.jet)
    plt.show()


def get_shape_from_experiment(run_input):
    horizontal = run_input['slice']['horizontal']['max'] - run_input['slice']['horizontal']['min']
    vertical = run_input['slice']['vertical']['max'] - run_input['slice']['vertical']['min']
    return vertical, horizontal


def get_profiles_length(profiles):
    shape = np.shape(profiles)
    if len(shape) == 3:
        return shape[0]
    if len(shape) == 2:
        return 1


def get_profiles_from_indices(indices_array, metadata_file, run_inputs_file, experiment_name):
    metadata_dict = json_tools.import_json_as_dict(metadata_file)
    address_list = beam_profile_metadata_tools.get_addresses_from_indices(indices_array, metadata_dict)
    run_input = json_tools.import_json_as_dict(run_inputs_file)[experiment_name]
    image_shape = get_shape_from_experiment(run_input)
    images = np.zeros(shape=(len(indices_array), image_shape[0], image_shape[1]))
    image_index = 0
    for run_list in address_list:
        if np.any(run_list):
            imported_profiles = beam_profiles_import_tool.get_specific_raw_beam_profiles(run_input, run_list)
            number_of_imported_profiles = get_profiles_length(imported_profiles)
            images[image_index:(number_of_imported_profiles + image_index)] = imported_profiles
            image_index += number_of_imported_profiles
    return images


def show_images(images, rows=1, title='test', save=False):
    n_images = len(images)
    fig = plt.figure()
    for n, image in enumerate(images):
        a = fig.add_subplot(rows, np.ceil(n_images / float(rows)), n + 1)
        a.axis('off')
        if n < np.ceil(n_images / float(rows)):
            a.set_title(str(n), loc='left')
        plt.imshow(image, cmap=plt.cm.jet)
    fig.suptitle(title)
    if save:
        plt.savefig('{}.png'.format(title))
    plt.show()
    plt.close()


if __name__ == '__main__':
    images = get_profiles_from_indices(['3_0', '3_1', '5_2', '5_1', '4_81', '4_2'],
                                       metadata_file='metadata_total.json',
                                       run_inputs_file='run_inputs.json',
                                       experiment_name='0')
    show_images(images)
