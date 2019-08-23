import beam_profile_metadata

if __name__ == '__main__':
    metadata_file = 'metadata/metadata.json'
    experiment_name = '0'
    run_inputs_file = 'metadata/run_inputs.json'
    masking_entries = beam_profile_metadata.MaskingIndexEntries(ring_thickness=10, number_of_tests=2,
                                                                experiment_name=experiment_name)
    area_perimeter_entries = beam_profile_metadata.AreaPerimeterIndexEntries(binarisation_fractions=[0.3, 0.5, 0.7],
                                                                             experiment_name=experiment_name)

    beam_profile_metadata.get_metadata_writer(None, None, metadata_file) \
        .add_labels_by_threshold(threshold=0.19, circularity_entries=masking_entries) \
        .add_labels_by_threshold(threshold=0.45, circularity_entries=area_perimeter_entries) \
        .add_labels_by_combination(circularity_entries_1=masking_entries,
                                   circularity_entries_2=area_perimeter_entries,
                                   label_name='combination_label') \
        .add_train_test_split(number_to_take=10000, label_name='combination_label', ratio_of_train=0.8,
                              ratio_of_1s=0.2) \
        .dump_metadata_to_json(filename=metadata_file, indent=2)
