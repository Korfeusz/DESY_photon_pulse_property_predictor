import numpy as np
import beam_profile_metadata
import json_tools

if __name__ == '__main__':
    run_numbers = [3]
    metadata_file = 'metadata/meta_test_1.json'
    for run_number in run_numbers:
        print('Started metadata analysis for run {}'.format(run_number))
        beam_profiles = np.load('preprocessed_data/beam_profiles_run_{}_small.npy'.format(run_number))
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
            .add_labels_by_threshold(threshold=10, circularity_entries=masking_entries) \
            .add_labels_by_threshold(threshold=5, circularity_entries=area_perimeter_entries) \
            .add_labels_by_combination(circularity_entries_1=masking_entries,
                                       circularity_entries_2=area_perimeter_entries,
                                       label_name='experimental_combo') \
            .dump_metadata_to_json(filename=metadata_file, indent=2)


    # worst_profiles, worst_indices = get_profiles_labeled_1_with_worst_index(metadata_dict, masking_entries_1,
    #                                                                         number_to_find=10)
    #
    # print(worst_indices)
    # print(worst_profiles)
    # images = beam_profile_imaging.get_profiles_from_indices(worst_profiles,
    #                                                         metadata_file=metadata_file,
    #                                                         run_inputs_file='metadata/run_inputs.json',
    #                                                         experiment_name='0')
    # beam_profile_imaging.show_images(images, rows=5)
