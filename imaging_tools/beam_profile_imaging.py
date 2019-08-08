import matplotlib.pyplot as plt
import numpy as np
from beam_profile_metadata import beam_profile_metadata_tools, json_tools
from beam_profiles_preprocessing import beam_profiles_import_tool


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
    for run_no, run_list in enumerate(address_list):
        if np.any(run_list):
            imported_profiles = beam_profiles_import_tool.get_specific_raw_beam_profiles(run_input, run_list, run_no)
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
    a = ['4_6258', '4_6194', '4_6195', '4_6196', '4_6197', '4_6198', '4_6199', '4_6200',
         '4_6201', '4_6202', '4_6203', '4_6204', '4_6205', '4_6206', '4_6207', '4_6208',
         '4_6209', '4_6210', '4_6211', '4_6212', '4_6213', '4_6214', '4_6193', '4_6215',
         '4_6192', '4_6190', '4_6169', '4_6170', '4_6171', '4_6172', '4_6173', '4_6174',
         '4_6175', '4_6176', '4_6177', '4_6178', '4_6179', '4_6180', '4_6181', '4_6182',
         '4_6183', '4_6184', '4_6185', '4_6186', '4_6187', '4_6188', '4_6189', '4_6191',
         '4_6216', '4_6217', '4_6218', '4_6269', '4_6268', '4_6267', '4_6266', '4_6265',
         '4_6264', '4_6263', '4_6262', '4_6261', '4_6260', '4_6259', '4_6226', '4_6257',
         '4_6227', '4_6255', '4_6239', '4_6238', '4_6237', '4_6236', '4_6240', '4_6234',
         '4_6270', '4_6271', '4_6272', '4_6273', '4_6219', '4_6220', '4_6221', '4_6222',
         '4_6223', '4_6224', '4_6225', '4_6167', '4_6286', '4_6228', '4_6168', '4_6285',
         '4_6283', '4_6282', '4_6281', '4_6280', '4_6279', '4_6278', '4_6277', '4_6276',
         '4_6275', '4_6274', '4_6284', '8_1726']
    images = get_profiles_from_indices(a,
                                       metadata_file='metadata_total.json',
                                       run_inputs_file='run_inputs.json',
                                       experiment_name='0')
    show_images(images, rows=10)
