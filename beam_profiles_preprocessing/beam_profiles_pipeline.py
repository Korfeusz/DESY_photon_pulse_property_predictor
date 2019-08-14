from beam_profiles_preprocessing import constants
import numpy as np
import image_manipulation_tools
import skimage


class BeamProfilesPipeline:
    def __init__(self, data, color_resolution=constants.BEAM_PROFILE_COLOR_RESOLUTION):
        self.beam_profile_data = data
        self.shape = np.shape(self.beam_profile_data)
        self.color_resolution = color_resolution

    def slice_horizontally(self, h_min, h_max):
        data = self.beam_profile_data[:, :, h_min:h_max]
        return BeamProfilesPipeline(data=data)

    def slice_vertically(self, v_min, v_max):
        data = self.beam_profile_data[:, v_min:v_max, :]
        return BeamProfilesPipeline(data=data)

    def change_color_resolution(self, new_resolution):
        data = image_manipulation_tools.change_color_resolution(self.beam_profile_data,
                                                                new_resolution,
                                                                self.color_resolution)
        color_resolution = new_resolution
        return BeamProfilesPipeline(data, color_resolution)

    def remove_background_by_intensity_fraction(self, cut_off_level):
        data = image_manipulation_tools.remove_background_by_intensity_fraction(self.beam_profile_data, cut_off_level)
        return BeamProfilesPipeline(data, self.color_resolution)

    def opening(self):
        data = image_manipulation_tools.grayscale_opening(self.beam_profile_data)
        return BeamProfilesPipeline(data, self.color_resolution)

    def shift_to_center_of_mass(self):
        data = image_manipulation_tools.shift_com_to_geometric(self.beam_profile_data)
        return BeamProfilesPipeline(data, self.color_resolution)

    def get_rounded_beam_profiles(self):
        return np.round(self.beam_profile_data)

    def rescale_images(self, horizontal_scale=1.1):
        data = skimage.transform.rescale(self.beam_profile_data, scale=(1, 1, horizontal_scale), multichannel=False)
        shape_corrected_data = data[:, :, :self.beam_profile_data.shape[-1]]
        return BeamProfilesPipeline(shape_corrected_data, color_resolution=self.color_resolution)

    def shift_to_highest_intensity(self, fraction):
        data = image_manipulation_tools.shift_highest_intensity_to_geometric(self.beam_profile_data, fraction=fraction)
        return BeamProfilesPipeline(data, self.color_resolution)

    def downsize_images(self, factor):
        data = skimage.transform.downscale_local_mean(self.beam_profile_data, factors=(1, factor, factor))
        return BeamProfilesPipeline(data, self.color_resolution)

