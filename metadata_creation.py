import numpy as np
import beam_profile_metadata
import json_tools

if __name__ == '__main__':
    run_numbers = [4]
    metadata_file = 'metadata/meta_test_2.json'
    for run_number in run_numbers:
        print('Started metadata analysis for run {}'.format(run_number))
        beam_profiles = np.load('/beegfs/desy/user/brockhul/preprocessed_data/beam_profiles_run_{}.npy'.format(run_number))
        beam_profiles = beam_profiles[0:2000]

        sums = np.sum(np.sum(beam_profiles, axis=2), axis=1)
        print(np.mean(sums))
        print(sums[953])
        print(sums[400])
        run_input = json_tools.import_json_as_dict('run_inputs/run_input_{}.json'.format(run_number))
        masking_entries = beam_profile_metadata.MaskingIndexEntries(ring_thickness=10, number_of_tests=2,
                                                                    experiment_name=run_input['experiment_name'])
        area_perimeter_entries = beam_profile_metadata.AreaPerimeterIndexEntries(binarisation_fractions=[0.3, 0.5, 0.7],
                                                                                 experiment_name=run_input[
                                                                                     'experiment_name'])
        beam_profile_metadata.get_metadata_writer(beam_profiles, run_input, metadata_file) \
            .add_beam_profiles_addresses() \
            .add_corrupted_label(threshold=1000) \
            .add_area_perimeter_squared_circularity_indices(binarisation_fractions=[0.3, 0.5]) \
            .add_masking_method_circularity_indices(ring_thickness=10, number_of_tests=2) \
            .add_masking_method_circularity_indices(ring_thickness=20, number_of_tests=2) \
            .add_area_perimeter_squared_circularity_indices(binarisation_fractions=[0.3, 0.5, 0.7]) \
            .dump_metadata_to_json(filename=metadata_file, indent=2)

