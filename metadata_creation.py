import numpy as np
import beam_profile_metadata
import json_tools

if __name__ == '__main__':
    run_numbers = [0, 1, 2, 3, 4, 5, 6, 7, 8]
    metadata_file = 'metadata/metadata.json'
    for run_number in run_numbers:
        print('Started metadata analysis for run {}'.format(run_number))
        beam_profiles = np.load('/beegfs/desy/user/brockhul/preprocessed_data/beam_profiles_run_{}.npy'.format(run_number))
        run_input = json_tools.import_json_as_dict('run_inputs/run_input_{}.json'.format(run_number))
        masking_entries = beam_profile_metadata.MaskingIndexEntries(ring_thickness=10, number_of_tests=2,
                                                                    experiment_name=run_input['experiment_name'])
        area_perimeter_entries = beam_profile_metadata.AreaPerimeterIndexEntries(binarisation_fractions=[0.3, 0.5, 0.7],
                                                                                 experiment_name=run_input[
                                                                                     'experiment_name'])
        beam_profile_metadata.get_metadata_writer(beam_profiles, run_input, metadata_file) \
            .add_beam_profiles_addresses() \
            .add_corrupted_label() \
            .add_area_perimeter_squared_circularity_indices(binarisation_fractions=[0.3, 0.5]) \
            .add_masking_method_circularity_indices(ring_thickness=10, number_of_tests=2) \
            .add_masking_method_circularity_indices(ring_thickness=20, number_of_tests=2) \
            .add_area_perimeter_squared_circularity_indices(binarisation_fractions=[0.3, 0.5, 0.7]) \
            .add_labels_by_threshold(threshold=0.4, circularity_entries=masking_entries) \
            .add_labels_by_threshold(threshold=0.7, circularity_entries=area_perimeter_entries) \
            .add_labels_by_combination(circularity_entries_1=masking_entries,
                                       circularity_entries_2=area_perimeter_entries,
                                       label_name='experimental_combo') \
            .add_train_test_split(number_to_take=100, label_name='experimental_combo') \
            .dump_metadata_to_json(filename=metadata_file, indent=2)

