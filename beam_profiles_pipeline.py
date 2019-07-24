import constants
import numpy as np


class BeamProfilesPipeline:
    def __init__(self, data, color_resolution=constants.BEAM_PROFILE_COLOR_RESOLUTION):
        self.beam_profile_data = data
        self.shape = self.beam_profile_data.shape
        self.color_resolution = color_resolution

    def slice_horizontally(self, h_min, h_max):
        return BeamProfilesPipeline(data=self.beam_profile_data[:, :, h_min:h_max])

    def slice_vertically(self, v_min, v_max):
        return BeamProfilesPipeline(data=self.beam_profile_data[:, v_min:v_max, :])

    def change_color_resolution(self, new_resolution):
        data = self.beam_profile_data / self.color_resolution * new_resolution
        color_resolution = new_resolution
        return BeamProfilesPipeline(data, color_resolution)

    def get_rounded_beam_profiles(self):
        return np.round(self.beam_profile_data)

