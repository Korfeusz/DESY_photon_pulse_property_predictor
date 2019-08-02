import area_perimeter_circle_finding_tool
import masking_method_circle_finding_tool


class BeamProfileMetadataWriter:
    def __init__(self, preprocessed_data, run_metadata, beam_profile_metadata_dict):
        self.data = preprocessed_data
        self.run_metadata = run_metadata
        self.beam_profile_metadata_dict = beam_profile_metadata_dict

    def add_area_perimeter_squared_circularity_indices(self, binarisation_fractions):
        indices = area_perimeter_circle_finding_tool.get_circularity_index(self.data, binarisation_fractions)
        type = 'area_perimeter'
        for i, index in enumerate(indices):
            self.beam_profile_metadata_dict


    def add_masking_method_circularity_indices(self):
        pass

    def add_beam_profiles_addresses(self):
        pass

    def add_labels(self):
        pass

    def add_train_test_split(self):
        pass
