import beam_profile_metadata

if __name__ == '__main__':
    metadata_file = 'metadata/meta_test_2.json'
    masking_entries = beam_profile_metadata.MaskingIndexEntries(ring_thickness=10, number_of_tests=2,
                                                                experiment_name='0')
    area_perimeter_entries = beam_profile_metadata.AreaPerimeterIndexEntries(binarisation_fractions=[0.3, 0.5, 0.7],
                                                                             experiment_name='0')

    beam_profile_metadata.get_metadata_writer(None, None, metadata_file) \
        .add_labels_by_threshold(threshold=0.2, circularity_entries=masking_entries) \
        .add_labels_by_threshold(threshold=0.4, circularity_entries=area_perimeter_entries) \
        .add_labels_by_combination(circularity_entries_1=masking_entries,
                                   circularity_entries_2=area_perimeter_entries,
                                   label_name='experimental_combo') \
        .add_train_test_split(number_to_take=100, label_name='experimental_combo') \
        .dump_metadata_to_json(filename=metadata_file, indent=2)
