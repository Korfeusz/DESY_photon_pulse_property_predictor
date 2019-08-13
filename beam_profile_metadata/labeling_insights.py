from beam_profile_metadata import tools
import numpy as np


def get_profiles_labeled_1_with_worst_index(metadata_dict, circularity_entries, number_to_find):
    profile_names, circularity_indices = get_profile_names_and_circularity_indices(circularity_entries, metadata_dict)
    indices_of_beam_profiles_labeled_1 = get_indices_of_beam_profiles_labeled_1(profile_names, metadata_dict,
                                                                                circularity_entries.index_string)
    beam_profiles_labeled_1 = fancy_index_list_and_convert_to_array(profile_names, indices_of_beam_profiles_labeled_1)
    circle_indices_of_beam_profiles_labeled_1 = fancy_index_list_and_convert_to_array(circularity_indices,
                                                                                      indices_of_beam_profiles_labeled_1)
    worst_indices = get_worst_indices(circle_indices_of_beam_profiles_labeled_1, number_to_find)
    return beam_profiles_labeled_1[worst_indices], circle_indices_of_beam_profiles_labeled_1[worst_indices]


def get_profile_names_and_circularity_indices(circularity_entries, metadata_dict):
    return list(zip(
        *list(circularity_entries.get_profile_names_and_their_circle_indices(metadata_dict))))


def get_indices_of_beam_profiles_labeled_1(profile_names, metadata_dict, index_string):
    return [i for i, p in enumerate(profile_names) if
            metadata_dict[p]['label'][index_string]['value'] == 1]


def fancy_index_list_and_convert_to_array(input_list, indices):
    return np.array(input_list)[indices]


def get_worst_indices(circle_indices, number_to_find):
    if len(circle_indices) < number_to_find:
        number_to_find = len(circle_indices)
    return tools.get_indices_of_n_highest_values(circle_indices,
                                                 number_to_find)
