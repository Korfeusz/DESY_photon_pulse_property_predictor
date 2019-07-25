import constants
import numpy as np
import background_remove_tools
import image_shifting

class BeamProfilesPipeline:
    def __init__(self, data, color_resolution=constants.BEAM_PROFILE_COLOR_RESOLUTION):
        self.beam_profile_data = data
        self.shape = np.shape(self.beam_profile_data)
        self.color_resolution = color_resolution

    def slice_horizontally(self, h_min, h_max):
        return BeamProfilesPipeline(data=self.beam_profile_data[:, :, h_min:h_max])

    def slice_vertically(self, v_min, v_max):
        return BeamProfilesPipeline(data=self.beam_profile_data[:, v_min:v_max, :])

    def change_color_resolution(self, new_resolution):
        data = background_remove_tools.change_color_resolution(self.beam_profile_data,
                                                               new_resolution,
                                                               self.color_resolution)
        color_resolution = new_resolution
        return BeamProfilesPipeline(data, color_resolution)

    def remove_background(self, number_of_lowest_colors=2, masking_color_resolution=7):
        data = background_remove_tools.remove_background(self.beam_profile_data,
                                                         initial_color_resolution=self.color_resolution,
                                                         processing_color_resolution=masking_color_resolution,
                                                         number_of_lowest_to_cut=number_of_lowest_colors)
        return BeamProfilesPipeline(data, self.color_resolution)

    def opening(self):
        return BeamProfilesPipeline(background_remove_tools.grayscale_opening(self.beam_profile_data),
                                    self.color_resolution)

    def shift_to_center_of_mass(self):
        return BeamProfilesPipeline(image_shifting.shift_com_to_geometric(self.beam_profile_data),
                                    self.color_resolution)

    def get_rounded_beam_profiles(self):
        return np.round(self.beam_profile_data)

