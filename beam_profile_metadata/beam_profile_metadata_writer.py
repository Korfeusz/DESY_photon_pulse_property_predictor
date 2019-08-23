from beam_profile_metadata import corrupted_image_finding_tools
from json_tools import json_tools
from beam_profile_metadata.circularity_index_entries import CircularityIndexEntries
from beam_profile_metadata.labeling import labeling_tools
from beam_profile_metadata import train_test_splitting_tools


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

    def add_train_test_split(self, number_to_take, label_name, ratio_of_train=0.5, ratio_of_1s=0.5):
        train_test_splitting_tools.train_test_split(self.beam_profile_metadata_dict, label_name, number_to_take, ratio_of_train, ratio_of_1s)
        return BeamProfileMetadataWriter(self.data, self.run_metadata, self.beam_profile_metadata_dict)

    def dump_metadata_to_json(self, filename, indent=None):
        json_tools.dump_dict_to_json(filename, self.beam_profile_metadata_dict, indent=indent)

    def add_corrupted_label(self, threshold):
        def corrupted_image_entry(i):
            self.get_profile_entry(i).setdefault('corrupted', bool)
            self.get_profile_entry(i)['corrupted'] = empty_images[i]

        empty_images = corrupted_image_finding_tools.find_empty_images(self.data, threshold)
        return self.add_value_to_runs(corrupted_image_entry, ignore_corrupted=False)
