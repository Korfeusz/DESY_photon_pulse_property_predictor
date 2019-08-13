import beam_profile_metadata
import imaging_tools
import json_tools

if __name__ == '__main__':
    metadata_file = 'metadata/meta_test_2.json'
    experiment_name = '0'
    run_inputs_file = 'metadata/run_inputs.json'

    metadata_dict = json_tools.import_json_as_dict(metadata_file)

    masking_entries = beam_profile_metadata.MaskingIndexEntries(ring_thickness=10, number_of_tests=2,
                                                                experiment_name=experiment_name)
    area_perimeter_entries = beam_profile_metadata.AreaPerimeterIndexEntries(binarisation_fractions=[0.3, 0.5, 0.7],
                                                                             experiment_name=experiment_name)


    worst_profiles, worst_indices = beam_profile_metadata.get_profiles_labeled_1_with_worst_index(metadata_dict,
                                                                                                  area_perimeter_entries,
                                                                                                  number_to_find=100,
                                                                                                  show_number_of_labeled_1=True)

    print('worst index: {}'.format(worst_indices[-1]))
    print('worst profile: {}'.format(worst_profiles[-1]))
    images = imaging_tools.get_profiles_from_indices(worst_profiles,
                                                     metadata_file=metadata_file,
                                                     run_inputs_file=run_inputs_file,
                                                     experiment_name=experiment_name)
    imaging_tools.show_images(images, rows=10)
