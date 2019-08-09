from imaging_tools import beam_profile_imaging
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


def get_profiles_with_existing_specific_labels(metadata_dict, index_string):
    return [p for p in metadata_dict if 'label' in metadata_dict[p] and index_string in metadata_dict[p]['label']]


def label_by_combination(metadata_dict, circularity_entries_1, circularity_entries_2, label_name):
    index_string_1 = circularity_entries_1.index_string
    index_string_2 = circularity_entries_2.index_string
    profiles_1 = get_profiles_with_existing_specific_labels(metadata_dict, index_string_1)
    profiles_2 = get_profiles_with_existing_specific_labels(metadata_dict, index_string_2)
    profiles_intersect = [p for p in profiles_1 if p in profiles_2]
    for profile in profiles_intersect:
        value = metadata_dict[profile]['label'][index_string_1]['value'] \
                or metadata_dict[profile]['label'][index_string_2]['value']
        dictionary_tools.insert_value_at_end_of_keys(metadata_dict[profile]['label'], keys=[label_name, 'value'],
                                                     value=value)


if __name__ == '__main__':
    from beam_profile_metadata.labeling_insights import get_profiles_labeled_1_with_worst_index
    metadata_file = 'metadata/meta_test.json'
    metadata_dict = json_tools.import_json_as_dict(metadata_file)
    area_perimeter_entries_1 = AreaPerimeterIndexEntries(binarisation_fractions=[0.3, 0.5, 0.7],
                                                         experiment_name='0')

    masking_entries_1 = MaskingIndexEntries(ring_thickness=20,
                                            number_of_tests=2,
                                            experiment_name='0')

    label_by_threshold(metadata_dict, area_perimeter_entries_1, threshold=0.32)
    label_by_threshold(metadata_dict, masking_entries_1, threshold=0.14)

    label_by_combination(metadata_dict, area_perimeter_entries_1, masking_entries_1, label_name='test_entry')

    json_tools.dump_dict_to_json(metadata_file, metadata_dict, indent=2)
    worst_profiles, worst_indices = get_profiles_labeled_1_with_worst_index(metadata_dict, masking_entries_1,
                                                                            number_to_find=10)

    print(worst_indices)
    print(worst_profiles)
    images = beam_profile_imaging.get_profiles_from_indices(worst_profiles,
                                                            metadata_file=metadata_file,
                                                            run_inputs_file='metadata/run_inputs.json',
                                                            experiment_name='0')
    beam_profile_imaging.show_images(images, rows=5)
