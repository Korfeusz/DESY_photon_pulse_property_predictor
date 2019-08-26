import numpy as np
import beam_profile_metadata
import json_tools
import constants

if __name__ == '__main__':
    run_numbers = [0, 1, 2, 3, 4, 5, 6, 7, 8]
    metadata_file = constants.metadata_file
    data_file_name = constants.preprocessed_beam_profiles_directory + '/beam_profiles_run_{}.npy'
    run_inputs_file = constants.run_input_file_template
    experiment_name = constants.experiment_name

    masking_entries = beam_profile_metadata.MaskingIndexEntries(ring_thickness=10, number_of_tests=2,
                                                                experiment_name=experiment_name)
    area_perimeter_entries = beam_profile_metadata.AreaPerimeterIndexEntries(binarisation_fractions=[0.3, 0.5, 0.7],
                                                                             experiment_name=experiment_name)

    for run_number in run_numbers:
        print('Started metadata analysis for run {}'.format(run_number))
        beam_profiles = np.load(data_file_name.format(run_number))
        run_input = json_tools.import_json_as_dict(run_inputs_file.format(run_number))

        beam_profile_metadata.get_metadata_writer(beam_profiles, run_input, metadata_file) \
            .add_beam_profiles_addresses() \
            .add_corrupted_label(threshold=1000) \
            .add_circularity_indices(masking_entries) \
            .add_circularity_indices(area_perimeter_entries) \
            .dump_metadata_to_json(filename=metadata_file, indent=2)
