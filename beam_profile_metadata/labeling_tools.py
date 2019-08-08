from beam_profile_metadata import beam_profile_metadata_tools


def get_specific_circle_indices_list(beam_profiles_metadata_dict, experiment_name,
                                     index_type,
                                     binarisation_fraction=None, ring_thickness=None,
                                     number_of_tests=None):
    beam_profiles_found = []
    circle_indices = []
    index_string = beam_profile_metadata_tools.get_circle_index_string(experiment_name, index_type, binarisation_fraction, ring_thickness,
                                                                       number_of_tests)

    for profile_index, profile_metadata in beam_profiles_metadata_dict.items():
        if not profile_metadata['corrupted'] and index_string in profile_metadata['circularity_index'].keys():
            beam_profiles_found.append(profile_index)
            circle_indices.append(profile_metadata['circularity_index'][index_string]['value'])
    return beam_profiles_found, circle_indices