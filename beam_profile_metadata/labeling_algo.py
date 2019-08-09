import numpy as np
from beam_profile_metadata.labeling_tools import get_specific_circle_indices_list
from imaging_tools import beam_profile_imaging
from beam_profile_metadata import beam_profile_metadata_tools, tools
from json_tools import json_tools
from beam_profile_metadata.circularity_index_entries import AreaPerimeterIndexEntries, MaskingIndexEntries
from beam_profile_metadata import dictionary_tools


def label_by_threshold(metadata_dict, circularity_entries, threshold):
    index_string = circularity_entries.index_string
    for profile, index in circularity_entries.get_profile_names_and_their_circle_indices(metadata_dict):
        dictionary_tools.insert_value_at_end_of_keys(metadata_dict, keys=[profile, 'label', index_string, 'value'],
                                                     value=int(index < threshold))
        dictionary_tools.insert_keyval_without_overwriting(metadata_dict[profile]['label'][index_string],
                                                           key='threshold', value=threshold)


def get_n_worst_label_1_profiles(beam_profiles_metadata_dict, number_to_find, experiment_name, index_type,
                                 binarisation_fraction=None,
                                 ring_thickness=None, number_of_tests=None):
    beam_profiles_found, circle_indices = get_specific_circle_indices_list(beam_profiles_metadata_dict,
                                                                           experiment_name,
                                                                           index_type,
                                                                           binarisation_fraction=binarisation_fraction,
                                                                           ring_thickness=ring_thickness,
                                                                           number_of_tests=number_of_tests)
    label_name = beam_profile_metadata_tools.get_circle_index_string(experiment_name=experiment_name,
                                                                     index_type=index_type,
                                                                     binarisation_fraction=binarisation_fraction,
                                                                     ring_thickness=ring_thickness,
                                                                     number_of_tests=number_of_tests)
    indices_of_beam_profiles_labeled_1 = [i for i, p in enumerate(beam_profiles_found) if
                                          beam_profiles_metadata_dict[p]['label'][label_name]['value'] == 1]
    print('Number of label 1s found: {}'.format(len(indices_of_beam_profiles_labeled_1)))
    print('Total number of profiles: {}'.format(len(beam_profiles_found)))
    if len(indices_of_beam_profiles_labeled_1) < number_to_find:
        number_to_find = len(indices_of_beam_profiles_labeled_1)
    beam_profiles_labeled_1 = np.array(beam_profiles_found)[indices_of_beam_profiles_labeled_1]
    circle_indices_of_beam_profiles_labeled_1 = np.array(circle_indices)[indices_of_beam_profiles_labeled_1]
    worst_indices = tools.get_indices_of_n_highest_values(np.array(circle_indices_of_beam_profiles_labeled_1),
                                                          number_to_find)
    return beam_profiles_labeled_1[worst_indices], circle_indices_of_beam_profiles_labeled_1[worst_indices]


if __name__ == '__main__':
    metadata_file = 'metadata/meta_test.json'
    metadata_dict = json_tools.import_json_as_dict(metadata_file)
    area_perimeter_entries_1 = AreaPerimeterIndexEntries(binarisation_fractions=[0.3, 0.5, 0.7],
                                                         experiment_name='0')

    masking_entries_1 = MaskingIndexEntries(ring_thickness=20,
                                            number_of_tests=2,
                                            experiment_name='0')

    label_by_threshold_2(metadata_dict, area_perimeter_entries_1, threshold=0.32)
    label_by_threshold_2(metadata_dict, masking_entries_1, threshold=14)

    json_tools.dump_dict_to_json(metadata_file, metadata_dict, indent=2)
    label_by_threshold(metadata_file,
                       threshold=0.1,
                       experiment_name='0',
                       index_type='masking',
                       ring_thickness=20,
                       number_of_tests=2,
                       indent=2)
    label_by_threshold(metadata_file,
                       threshold=0.46,
                       experiment_name='0',
                       index_type='area_perimeter',
                       binarisation_fraction=[0.3, 0.5, 0.7],
                       indent=2)

    # Create a combined label
    label_name = 'combined_label_test_name'
    label_description = 'experimental combined label'
    circle_index_data_1 = {'experiment_name': '0',
                           'index_type': 'masking',
                           'ring_thickness': 20,
                           'number_of_tests': 2}
    circle_index_string_1 = beam_profile_metadata_tools.get_circle_index_string(**circle_index_data_1)
    circle_index_data_2 = {'experiment_name': '0',
                           'index_type': 'area_perimeter',
                           'binarisation_fraction': [0.3, 0.5, 0.7]}
    circle_index_string_2 = beam_profile_metadata_tools.get_circle_index_string(**circle_index_data_2)
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
                                                                 **circle_index_data_1)
    print(worst_indices)
    print(worst_profiles)
    images = beam_profile_imaging.get_profiles_from_indices(worst_profiles,
                                                            metadata_file=metadata_file,
                                                            run_inputs_file='run_inputs.json',
                                                            experiment_name='0')
    beam_profile_imaging.show_images(images, rows=10)
