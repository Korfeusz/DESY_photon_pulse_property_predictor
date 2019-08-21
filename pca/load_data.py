def get_codes_file(metadata_dict):
    for index, values in metadata_dict.items():
        if 'autoencoder' in values.keys():
            return values['autoencoder']['code_file']


def get_profile_indices_and_corresponding_code_indices(metadata_dict):
    indices = []
    code_indices = []
    for index, values in metadata_dict.items():
        if 'autoencoder' in values.keys():
            indices.append(index)
            code_indices.append(values['autoencoder']['code_index'])
    return indices, code_indices
