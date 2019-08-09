from abc import ABC, abstractmethod


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
    def get_profiles(self, metadata_dict):
        for profile_index, profile_metadata in metadata_dict.items():
            if not profile_metadata['corrupted'] and self.index_string in profile_metadata['circularity_index'].keys():
                yield profile_index

    @abstractmethod
    def get_circle_indices(self, metadata_dict):
        for profile_index, profile_metadata in metadata_dict.items():
            if not profile_metadata['corrupted'] and self.index_string in profile_metadata['circularity_index'].keys():
                yield profile_metadata['circularity_index'][self.index_string]['value']

    @property
    @abstractmethod
    def settings(self):
        pass

    @property
    @abstractmethod
    def experiment_name(self):
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

    def get_circle_indices(self, metadata_dict):
        return super().get_circle_indices(metadata_dict)

    def get_profiles(self, metadata_dict):
        return super().get_profiles(metadata_dict)


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

    def get_circle_indices(self, metadata_dict):
        return super().get_circle_indices(metadata_dict)

    def get_profiles(self, metadata_dict):
        return super().get_profiles(metadata_dict)


if __name__ == '__main__':
    from json_tools import import_json_as_dict
    dic = import_json_as_dict('../metadata/meta_test.json')
    a = AreaPerimeterIndexEntries(binarisation_fractions=[0.3, 0.5, 0.7], experiment_name='0')
    b = MaskingIndexEntries(experiment_name='0', ring_thickness=20, number_of_tests=2)
    l = list(a.get_profiles(dic))
    print(l[:10])
    print(type(a.get_profiles(dic)))

    l = list(b.get_profiles(dic))
    print(l[:10])
    print(type(b.get_profiles(dic)))
