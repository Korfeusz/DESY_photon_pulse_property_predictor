from beam_profile_metadata import tools
import numpy as np





def get_profiles_labeled_1_with_worst_index(metadata_dict, circularity_entries, number_to_find):
    profile_names, circularity_indices = list(zip(
        *list(circularity_entries.get_profile_names_and_their_circle_indices(metadata_dict))))
    index_string = circularity_entries.index_string
    indices_of_beam_profiles_labeled_1 = [i for i, p in enumerate(profile_names) if
                                          metadata_dict[p]['label'][index_string]['value'] == 1]

    if len(indices_of_beam_profiles_labeled_1) < number_to_find:
        number_to_find = len(indices_of_beam_profiles_labeled_1)

    beam_profiles_labeled_1 = np.array(profile_names)[indices_of_beam_profiles_labeled_1]
    circle_indices_of_beam_profiles_labeled_1 = np.array(circularity_indices)[indices_of_beam_profiles_labeled_1]
    worst_indices = tools.get_indices_of_n_highest_values(np.array(circle_indices_of_beam_profiles_labeled_1),
                                                          number_to_find)
    return beam_profiles_labeled_1[worst_indices], circle_indices_of_beam_profiles_labeled_1[worst_indices]
