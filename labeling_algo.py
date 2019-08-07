import json_tools
import tools
import numpy as np


def get_specific_circle_indices_list(beam_profiles_metadata_dict, experiment_name,
                                     index_type,
                                     binarisation_fraction=None, ring_thickness=None,
                                     number_of_tests=None):
    beam_profiles_found = []
    circle_indices = []
    index_string = get_circle_index_string(experiment_name, index_type, binarisation_fraction, ring_thickness,
                                           number_of_tests)

    for profile_index, profile_metadata in beam_profiles_metadata_dict.items():
        if index_string in profile_metadata['circularity_index'].keys():
            beam_profiles_found.append(profile_index)
            circle_indices.append(profile_metadata['circularity_index'][index_string]['value'])
    return beam_profiles_found, circle_indices


def get_circle_index_string(experiment_name, index_type, binarisation_fraction=None, ring_thickness=None,
                            number_of_tests=None):
    if index_type == 'area_perimeter':
        settings_string = '_'.join([str(x - int(x)).split('.')[1] for x in binarisation_fraction])
    elif index_type == 'masking':
        settings_string = '_'.join([str(ring_thickness), str(number_of_tests)])
    return 'run_name_{}_{}_settings_{}'.format(experiment_name, index_type, settings_string)


def get_split_above_and_below_threshold(beam_profiles, circle_indices, threshold):
    above_threshold = [profile for profile, circ_index in zip(beam_profiles, circle_indices) if circ_index > threshold]
    below_threshold = [profile for profile in beam_profiles if profile not in above_threshold]
    return above_threshold, below_threshold


def label_by_threshold(metadata_file, experiment_name, index_type, threshold, binarisation_fraction=None,
                       ring_thickness=None,
                       number_of_tests=None,
                       indent=None):
    metadata_dict = json_tools.import_json_as_dict(metadata_file)
    profiles, circularity_indices_m1 = get_specific_circle_indices_list(metadata_dict,
                                                                        experiment_name=experiment_name,
                                                                        index_type=index_type,
                                                                        binarisation_fraction=binarisation_fraction,
                                                                        ring_thickness=ring_thickness,
                                                                        number_of_tests=number_of_tests)
    above_threshold_m1, below_threshold_m1 = get_split_above_and_below_threshold(profiles,
                                                                                 circularity_indices_m1,
                                                                                 threshold=threshold)
    index_string = get_circle_index_string(experiment_name=experiment_name, index_type=index_type,
                                           binarisation_fraction=binarisation_fraction,
                                           ring_thickness=ring_thickness,
                                           number_of_tests=number_of_tests)

    for profile in profiles:
        metadata_dict[profile].setdefault('label', {})
        metadata_dict[profile]['label'].setdefault(index_string, {})
        metadata_dict[profile]['label'][index_string].setdefault('value', int)
        if profile in below_threshold_m1:
            metadata_dict[profile]['label'][index_string]['value'] = 1
        else:
            metadata_dict[profile]['label'][index_string]['value'] = 0
        metadata_dict[profile]['label'][index_string].setdefault('threshold', float)
        metadata_dict[profile]['label'][index_string]['threshold'] = threshold
    json_tools.dump_dict_to_json(metadata_file, metadata_dict, indent=indent)


def get_n_worst_label_1_profiles(beam_profiles_metadata_dict, number_to_find, experiment_name, index_type,
                                 binarisation_fraction=None,
                                 ring_thickness=None, number_of_tests=None):
    beam_profiles_found, circle_indices = get_specific_circle_indices_list(beam_profiles_metadata_dict,
                                                                           experiment_name,
                                                                           index_type,
                                                                           binarisation_fraction=binarisation_fraction,
                                                                           ring_thickness=ring_thickness,
                                                                           number_of_tests=number_of_tests)
    label_name = get_circle_index_string(experiment_name=experiment_name, index_type=index_type,
                                         binarisation_fraction=binarisation_fraction,
                                         ring_thickness=ring_thickness,
                                         number_of_tests=number_of_tests)
    indices_of_beam_profiles_labeled_1 = [i for i, p in enumerate(beam_profiles_found) if beam_profiles_metadata_dict[p]['label'][label_name]['value'] == 1]
    beam_profiles_labeled_1 = np.array(beam_profiles_found)[indices_of_beam_profiles_labeled_1]
    circle_indices_of_beam_profiles_labeled_1 = np.array(circle_indices)[indices_of_beam_profiles_labeled_1]
    worst_indices = tools.get_indices_of_n_highest_values(np.array(circle_indices_of_beam_profiles_labeled_1),
                                                          number_to_find)
    return beam_profiles_labeled_1[worst_indices], circle_indices_of_beam_profiles_labeled_1[worst_indices]


if __name__ == '__main__':
    metadata_file = 'metadata_total.json'

    label_by_threshold(metadata_file,
                       threshold=0.4,
                       experiment_name='0',
                       index_type='masking',
                       ring_thickness=20,
                       number_of_tests=2,
                       indent=2)
    label_by_threshold(metadata_file,
                       threshold=0.2,
                       experiment_name='0',
                       index_type='area_perimeter',
                       binarisation_fraction=[0.3, 0.5],
                       indent=2)

    # Create a combined label
    label_name = 'combined_label_test_name'
    label_description = 'experimental combined label'
    circle_index_data_1 = {'experiment_name': '0',
                           'index_type': 'masking',
                           'ring_thickness': 10,
                           'number_of_tests': 2}
    circle_index_string_1 = get_circle_index_string(**circle_index_data_1)
    circle_index_data_2 = {'experiment_name': '0',
                           'index_type': 'area_perimeter',
                           'binarisation_fraction': [0.3, 0.5]}
    circle_index_string_2 = get_circle_index_string(**circle_index_data_2)
    metadata_dict = json_tools.import_json_as_dict(metadata_file)
    for profile_index, profile_metadata in metadata_dict.items():
        if 'label' in profile_metadata.keys():
            if (circle_index_string_1 in profile_metadata['label'].keys()) \
                    and (circle_index_string_2 in profile_metadata['label'].keys()):
                label = profile_metadata['label'][circle_index_string_1]['value'] \
                        or profile_metadata['label'][circle_index_string_2]['value']
                profile_metadata['label'].setdefault(label_name, {})
                profile_metadata['label'][label_name].setdefault('value', int)
                profile_metadata['label'][label_name]['value'] = label
                profile_metadata['label'][label_name].setdefault('description', str)
                profile_metadata['label'][label_name]['description'] = label_description

    json_tools.dump_dict_to_json(metadata_file, metadata_dict, indent=2)

    metadata_dict = json_tools.import_json_as_dict(metadata_file)
    worst_profiles, worst_indices = get_n_worst_label_1_profiles(metadata_dict, number_to_find=100,
                                                                 **circle_index_data_2)
    print(worst_indices)
    print(worst_profiles)
