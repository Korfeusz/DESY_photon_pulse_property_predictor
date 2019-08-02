import area_perimeter_circle_finding_tool
import masking_method_circle_finding_tool
import json_tools

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

    def add_value_to_runs(self, entry_inserting_function):
        for i in range(len(self.data)):
            self.insert_beam_profile_index(i)
            entry_inserting_function(i)
        return BeamProfileMetadataWriter(self.data, self.run_metadata, self.beam_profile_metadata_dict)

    def add_area_perimeter_squared_circularity_indices(self, binarisation_fractions):
        def area_perimeter_entry(i):
            self.get_profile_entry(i).setdefault('circularity_index', []).append({
                'type': 'area_perimeter',
                'settings': binarisation_fractions,
                'pipeline_settings_name': self.run_metadata['experiment_name'],
                'value': indices[i]
            })
        indices = area_perimeter_circle_finding_tool.get_circularity_index(self.data, binarisation_fractions)
        return self.add_value_to_runs(area_perimeter_entry)

    def add_masking_method_circularity_indices(self, ring_thickness=20, number_of_tests=2):
        def masking_entry(i):
            self.get_profile_entry(i).setdefault('circularity_index', []).append({
                'type': 'masking',
                'settings': {'ring_thickness': ring_thickness,
                             'number_of_tests': number_of_tests},
                'pipeline_settings_name': self.run_metadata['experiment_name'],
                'value': indices[i]
            })

        indices = masking_method_circle_finding_tool.is_circle_in_center_of_images(self.data,
                                                                                   ring_thickness,
                                                                                   number_of_tests)
        return self.add_value_to_runs(masking_entry)

    def add_beam_profiles_addresses(self):
        def address_entry(i):
            entry = {'run': self.run_metadata['run_number'], 'profile_number': i}
            self.get_profile_entry(i).setdefault('address', entry)
        return self.add_value_to_runs(address_entry)

    def add_labels(self):
        pass

    def add_train_test_split(self):
        pass

    def dump_metadata_to_json(self, filename, indent=None):
        json_tools.dump_dict_to_json(filename, self.beam_profile_metadata_dict, indent=indent)
