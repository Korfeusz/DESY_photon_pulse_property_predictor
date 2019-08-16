from abc import ABC, abstractmethod
from circle_finding_tools import masking_method_circle_finding_tool, area_perimeter_circle_finding_tool


class CircularityIndexEntries(ABC):
    @property
    @abstractmethod
    def index_string(self):
        pass

    @property
    @abstractmethod
    def type_of_index(self):
        pass

    @abstractmethod
    def get_profile_names_and_their_circle_indices(self, metadata_dict):
        for profile_index, profile_metadata in metadata_dict.items():
            if not profile_metadata['corrupted'] and self.index_string in profile_metadata['circularity_index'].keys():
                yield profile_index, profile_metadata['circularity_index'][self.index_string]['value']


    @property
    @abstractmethod
    def settings(self):
        pass

    @property
    @abstractmethod
    def experiment_name(self):
        pass

    @abstractmethod
    def calculate_indices(self, data):
        pass


class AreaPerimeterIndexEntries(CircularityIndexEntries):
    def __init__(self, binarisation_fractions, experiment_name):
        self.binarisation_fractions = binarisation_fractions
        self._experiment_name = experiment_name
        self._index_string = self.create_index_string()

    def create_index_string(self):
        settings_string = '_'.join([str(x - int(x)).split('.')[1] for x in self.settings])
        return 'run_name_{}_{}_settings_{}'.format(self.experiment_name, self.type_of_index, settings_string)

    @property
    def index_string(self):
        return self._index_string

    @property
    def type_of_index(self):
        return 'area_perimeter'

    @property
    def settings(self):
        return self.binarisation_fractions

    @property
    def experiment_name(self):
        return self._experiment_name

    def get_profile_names_and_their_circle_indices(self, metadata_dict):
        return super().get_profile_names_and_their_circle_indices(metadata_dict)

    def calculate_indices(self, data):
        return area_perimeter_circle_finding_tool.get_circularity_index(data=data,
                                                                        binarisation_fractions=self.binarisation_fractions)


class MaskingIndexEntries(CircularityIndexEntries):
    def __init__(self, ring_thickness, number_of_tests, experiment_name):
        self.ring_thickness = ring_thickness
        self.number_of_tests = number_of_tests
        self._experiment_name = experiment_name
        self._index_string = self.create_index_string()

    def create_index_string(self):
        settings_string = '_'.join([str(self.ring_thickness), str(self.number_of_tests)])
        return 'run_name_{}_{}_settings_{}'.format(self.experiment_name, self.type_of_index, settings_string)

    @property
    def index_string(self):
        return self._index_string

    @property
    def type_of_index(self):
        return 'masking'

    @property
    def settings(self):
        return {
          "ring_thickness": self.ring_thickness,
          "number_of_tests": self.number_of_tests
        }

    @property
    def experiment_name(self):
        return self._experiment_name

    def get_profile_names_and_their_circle_indices(self, metadata_dict):
        return super().get_profile_names_and_their_circle_indices(metadata_dict)

    def calculate_indices(self, data):
        return masking_method_circle_finding_tool.is_circle_in_center_of_images(data=data,
                                                                                ring_thickness=self.ring_thickness,
                                                                                number_of_tests=self.number_of_tests)


if __name__ == '__main__':
    from json_tools import import_json_as_dict
    dic = import_json_as_dict('../metadata/meta_test.json')
    a = AreaPerimeterIndexEntries(binarisation_fractions=[0.3, 0.5, 0.7], experiment_name='0')
    b = MaskingIndexEntries(experiment_name='0', ring_thickness=20, number_of_tests=2)
    l = list(a.get_profile_names_and_their_circle_indices(dic))
    print(l[:10])
    print(type(a.get_profile_names_and_their_circle_indices(dic)))

    l = list(b.get_profile_names_and_their_circle_indices(dic))
    print(l[:10])
    print(type(b.get_profile_names_and_their_circle_indices(dic)))
