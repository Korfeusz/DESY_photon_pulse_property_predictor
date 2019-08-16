from circle_finding_tools import masking_method_circle_finding_tool, area_perimeter_circle_finding_tool
from beam_profile_metadata import corrupted_image_finding_tools, beam_profile_metadata_tools
from json_tools import json_tools
from beam_profile_metadata.circularity_index_entries import CircularityIndexEntries
from beam_profile_metadata import labeling_tools
from beam_profile_metadata import train_test_splitting_tools
# from beam_profile_metadata import dictionary_tools
#
#
# def insert_index_outside_list(list, index, value):
#     if index >= len(list):
#         list.extend([None for _ in range(index - len(list) + 1)])
#     list[index] = value
#
# def add_to_list_if_too_short(items, index, item_to_pad=None):
#     if index >= len(items):
#         items.extend([item_to_pad for _ in range(index - len(items) + 1)])

# class BeamProfileMetadataWriter2:
#     def __init__(self, preprocessed_data_for_one_run, run_metadata, beam_profile_metadata):
#         self.data = preprocessed_data_for_one_run
#         self.run_metadata = run_metadata
#         add_to_list_if_too_short(beam_profile_metadata, run_metadata['run_number'], item_to_pad=[])
#         self.beam_profile_metadata = beam_profile_metadata
#
#
#     def add_circularity_indices(self, circularity_entries: CircularityIndexEntries):
#         indices = circularity_entries.calculate_indices(self.data)
#         list_to_enter = [{circularity_entries.index_string: {
#             'type': circularity_entries.type_of_index,
#             'settings': circularity_entries.settings,
#             'pipeline_settings_name': self.run_metadata['experiment_name'],
#             'value': idx
#         }} for idx in indices]


class BeamProfileMetadataWriter:
    def __init__(self, preprocessed_data, run_metadata, beam_profile_metadata_dict):
        self.data = preprocessed_data
        self.run_metadata = run_metadata
        self.beam_profile_metadata_dict = beam_profile_metadata_dict

    def get_run_image_index_string(self, image_number):
        return '{}_{}'.format(self.run_metadata['run_number'], image_number)

    def insert_beam_profile_index(self, profile_number):
        return self.beam_profile_metadata_dict.setdefault(self.get_run_image_index_string(profile_number), {})

    def get_profile_entry(self, profile_number):
        return self.beam_profile_metadata_dict[self.get_run_image_index_string(profile_number)]

    def is_image_corrupted(self, i):
        if 'corrupted' in self.get_profile_entry(i).keys():
            return self.get_profile_entry(i)['corrupted']

    def add_value_to_runs(self, entry_inserting_function, ignore_corrupted=False):
        for i in range(len(self.data)):
            if ignore_corrupted and self.is_image_corrupted(i):
                continue
            self.insert_beam_profile_index(i)
            entry_inserting_function(i)
        return BeamProfileMetadataWriter(self.data, self.run_metadata, self.beam_profile_metadata_dict)

    # def get_circle_index_string(self, index_type, binarisation_fraction=None, ring_thickness=None,
    #                             number_of_tests=None):
    #     return beam_profile_metadata_tools.get_circle_index_string(self.run_metadata['experiment_name'],
    #                                                                index_type, binarisation_fraction, ring_thickness, number_of_tests)

    def add_circularity_indices(self, circularity_entries: CircularityIndexEntries):
        def circularity_entry(i):
            self.get_profile_entry(i).setdefault('circularity_index', {})
            index_string = circularity_entries.index_string
            self.get_profile_entry(i)['circularity_index'].setdefault(index_string, {})
            self.get_profile_entry(i)['circularity_index'][index_string] = {
                'type': 'area_perimeter',
                'settings': circularity_entries.settings,
                'pipeline_settings_name': self.run_metadata['experiment_name'],
                'value': indices[i]
            }
        indices = circularity_entries.calculate_indices(self.data)
        return self.add_value_to_runs(circularity_entry, ignore_corrupted=True)



    # def add_area_perimeter_squared_circularity_indices(self, binarisation_fractions):
    #     def area_perimeter_entry(i):
    #         self.get_profile_entry(i).setdefault('circularity_index', {})
    #         index_string = self.get_circle_index_string(index_type='area_perimeter',
    #                                                     binarisation_fraction=binarisation_fractions)
    #         self.get_profile_entry(i)['circularity_index'].setdefault(index_string, {})
    #         self.get_profile_entry(i)['circularity_index'][index_string] = {
    #             'type': 'area_perimeter',
    #             'settings': binarisation_fractions,
    #             'pipeline_settings_name': self.run_metadata['experiment_name'],
    #             'value': indices[i]
    #         }
    #
    #     indices = area_perimeter_circle_finding_tool.get_circularity_index(self.data, binarisation_fractions)
    #     return self.add_value_to_runs(area_perimeter_entry, ignore_corrupted=True)
    #
    # def add_masking_method_circularity_indices(self, ring_thickness=20, number_of_tests=2):
    #     def masking_entry(i):
    #         self.get_profile_entry(i).setdefault('circularity_index', {})
    #         index_string = self.get_circle_index_string(index_type='masking',
    #                                                     ring_thickness=ring_thickness,
    #                                                     number_of_tests=number_of_tests)
    #         self.get_profile_entry(i)['circularity_index'].setdefault(index_string, {})
    #         self.get_profile_entry(i)['circularity_index'][index_string] = {
    #             'type': 'masking',
    #             'settings': {'ring_thickness': ring_thickness,
    #                          'number_of_tests': number_of_tests},
    #             'pipeline_settings_name': self.run_metadata['experiment_name'],
    #             'value': indices[i]
    #         }
    #
    #     indices = masking_method_circle_finding_tool.is_circle_in_center_of_images(self.data,
    #                                                                                ring_thickness,
    #                                                                                number_of_tests)
    #     return self.add_value_to_runs(masking_entry, ignore_corrupted=True)

    def add_beam_profiles_addresses(self):
        def address_entry(i):
            entry = {'run': self.run_metadata['run_number'], 'profile_number': i}
            self.get_profile_entry(i).setdefault('address', {})
            self.get_profile_entry(i)['address'] = entry

        return self.add_value_to_runs(address_entry, ignore_corrupted=False)

    def add_labels_by_threshold(self, threshold, circularity_entries: CircularityIndexEntries):
        labeling_tools.label_by_threshold(self.beam_profile_metadata_dict, circularity_entries, threshold)
        return BeamProfileMetadataWriter(self.data, self.run_metadata, self.beam_profile_metadata_dict)

    def add_labels_by_combination(self, circularity_entries_1, circularity_entries_2, label_name):
        labeling_tools.label_by_combination(self.beam_profile_metadata_dict, circularity_entries_1, circularity_entries_2, label_name)
        return BeamProfileMetadataWriter(self.data, self.run_metadata, self.beam_profile_metadata_dict)

    def add_train_test_split(self, number_to_take, label_name, ratio_of_train=0.5):
        train_test_splitting_tools.train_test_split(self.beam_profile_metadata_dict, label_name, number_to_take, ratio_of_train)
        return BeamProfileMetadataWriter(self.data, self.run_metadata, self.beam_profile_metadata_dict)

    def dump_metadata_to_json(self, filename, indent=None):
        json_tools.dump_dict_to_json(filename, self.beam_profile_metadata_dict, indent=indent)

    def add_corrupted_label(self, threshold):
        def corrupted_image_entry(i):
            self.get_profile_entry(i).setdefault('corrupted', bool)
            self.get_profile_entry(i)['corrupted'] = empty_images[i]

        empty_images = corrupted_image_finding_tools.find_empty_images(self.data, threshold)
        return self.add_value_to_runs(corrupted_image_entry, ignore_corrupted=False)
