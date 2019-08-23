from beam_profile_metadata.circularity_index_entries import CircularityIndexEntries
from beam_profile_metadata.tools import dictionary_tools


def label_by_threshold(metadata_dict, circularity_entries: CircularityIndexEntries, threshold):
    index_string = circularity_entries.index_string
    for profile, index in circularity_entries.get_profile_names_and_their_circle_indices(metadata_dict):
        dictionary_tools.insert_value_at_end_of_keys(metadata_dict, keys=[profile, 'label', index_string, 'value'],
                                                     value=int(index < threshold))
        dictionary_tools.insert_keyval_without_overwriting(metadata_dict[profile]['label'][index_string],
                                                           key='threshold', value=threshold)


def get_profiles_with_existing_specific_labels(metadata_dict, index_string):
    return [p for p in metadata_dict if 'label' in metadata_dict[p] and index_string in metadata_dict[p]['label']]


def label_by_combination(metadata_dict, circularity_entries_1: CircularityIndexEntries,
                         circularity_entries_2: CircularityIndexEntries, label_name):
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
