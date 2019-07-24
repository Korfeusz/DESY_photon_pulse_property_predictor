import constants
import numpy as np


class BeamProfileCreator:
    def __init__(self, data, color_resolution=constants.BEAM_PROFILE_COLOR_RESOLUTION):
        self.beam_profile_data = data
        self.shape = self.beam_profile_data.shape
        self.color_resolution = color_resolution

    def slice_horizontally(self, h_min, h_max):
        return BeamProfileCreator(data=self.beam_profile_data[:, h_min:h_max])

    def slice_vertically(self, v_min, v_max):
        return BeamProfileCreator(data=self.beam_profile_data[v_min:v_max])

    def change_color_resolution(self, new_resolution):
        data = self.beam_profile_data / self.color_resolution * new_resolution
        color_resolution = new_resolution
        return BeamProfileCreator(data, color_resolution)

    def get_beam_profile_rounded_to_int(self):
        return self.beam_profile_data.astype(np.int)
