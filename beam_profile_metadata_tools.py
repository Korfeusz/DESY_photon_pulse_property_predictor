import beam_profile_metadata_writer
import json_tools


def get_metadata_writer(beam_profiles, run_input, metadata_filename):
    beam_profile_metadata_dict = json_tools.import_json_as_dict(metadata_filename)
    return beam_profile_metadata_writer.BeamProfileMetadataWriter(beam_profiles, run_input, beam_profile_metadata_dict)
