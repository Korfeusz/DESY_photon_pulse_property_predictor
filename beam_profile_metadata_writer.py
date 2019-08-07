import area_perimeter_circle_finding_tool
import beam_profile_metadata_tools
import masking_method_circle_finding_tool
import json_tools
import labeling_algo
import corrupted_image_finding_tools

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

    def get_circle_index_string(self, index_type, binarisation_fraction=None, ring_thickness=None,
                                number_of_tests=None):
        return beam_profile_metadata_tools.get_circle_index_string(self.run_metadata['experiment_name'],
                                                                   index_type, binarisation_fraction, ring_thickness, number_of_tests)

    def add_area_perimeter_squared_circularity_indices(self, binarisation_fractions):
        def area_perimeter_entry(i):
            self.get_profile_entry(i).setdefault('circularity_index', {})
            index_string = self.get_circle_index_string(index_type='area_perimeter',
                                                        binarisation_fraction=binarisation_fractions)
            self.get_profile_entry(i)['circularity_index'].setdefault(index_string, {})
            self.get_profile_entry(i)['circularity_index'][index_string] = {
                'type': 'area_perimeter',
                'settings': binarisation_fractions,
                'pipeline_settings_name': self.run_metadata['experiment_name'],
                'value': indices[i]
            }

        indices = area_perimeter_circle_finding_tool.get_circularity_index(self.data, binarisation_fractions)
        return self.add_value_to_runs(area_perimeter_entry, ignore_corrupted=True)

    def add_masking_method_circularity_indices(self, ring_thickness=20, number_of_tests=2):
        def masking_entry(i):
            self.get_profile_entry(i).setdefault('circularity_index', {})
            index_string = self.get_circle_index_string(index_type='masking',
                                                        ring_thickness=ring_thickness,
                                                        number_of_tests=number_of_tests)
            self.get_profile_entry(i)['circularity_index'].setdefault(index_string, {})
            self.get_profile_entry(i)['circularity_index'][index_string] = {
                'type': 'masking',
                'settings': {'ring_thickness': ring_thickness,
                             'number_of_tests': number_of_tests},
                'pipeline_settings_name': self.run_metadata['experiment_name'],
                'value': indices[i]
            }

        indices = masking_method_circle_finding_tool.is_circle_in_center_of_images(self.data,
                                                                                   ring_thickness,
                                                                                   number_of_tests)
        return self.add_value_to_runs(masking_entry, ignore_corrupted=True)

    def add_beam_profiles_addresses(self):
        def address_entry(i):
            entry = {'run': self.run_metadata['run_number'], 'profile_number': i}
            self.get_profile_entry(i).setdefault('address', {})
            self.get_profile_entry(i)['address'] = entry

        return self.add_value_to_runs(address_entry, ignore_corrupted=False)

    def add_labels(self):
        pass

    def add_train_test_split(self):
        pass

    def dump_metadata_to_json(self, filename, indent=None):
        json_tools.dump_dict_to_json(filename, self.beam_profile_metadata_dict, indent=indent)

    def add_corrupted_label(self):
        def corrupted_image_entry(i):
            self.get_profile_entry(i).setdefault('corrupted', bool)
            self.get_profile_entry(i)['corrupted'] = empty_images[i]

        empty_images = corrupted_image_finding_tools.find_empty_images(self.data)
        return self.add_value_to_runs(corrupted_image_entry, ignore_corrupted=False)
