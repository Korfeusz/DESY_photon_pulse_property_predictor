import numpy as np


def get_specific_circle_indeces_list(beam_profiles_metadata_dict, index_settings):
    beam_profiles_found = []
    circle_indices = []
    for profile_index, profile_metadata in beam_profiles_metadata_dict.items():
        for index_data in profile_metadata['circularity_index']:
            if index_data['settings'] == index_settings:
                beam_profiles_found.append(profile_index)
                circle_indices.append(index_data['value'])
    return beam_profiles_found, circle_indices
