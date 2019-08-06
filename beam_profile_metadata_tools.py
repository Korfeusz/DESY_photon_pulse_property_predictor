import beam_profile_metadata_writer
import json_tools
import constants


def get_metadata_writer(beam_profiles, run_input, metadata_filename):
    beam_profile_metadata_dict = json_tools.import_json_as_dict(metadata_filename)
    return beam_profile_metadata_writer.BeamProfileMetadataWriter(beam_profiles, run_input, beam_profile_metadata_dict)


def get_run_input_from_run_name(run_name, run_inputs_file):
    run_inputs_dict = json_tools.import_json_as_dict(run_inputs_file)
    return run_inputs_dict[run_name]


def get_addresses_from_indices(indices, metadata_dict):
    address_list = [[] for _ in range(constants.NUMBER_OF_RUNS)]
    for index in indices:
        address = metadata_dict[index]['address']
        address_list[address['run']].append(address['profile_number'])
    return address_list
