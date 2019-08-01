import time

import constants
import numpy as np
import background_remove_tools
import image_shifting
import skimage


class BeamProfilesPipeline:
    def __init__(self, data, color_resolution=constants.BEAM_PROFILE_COLOR_RESOLUTION):
        self.beam_profile_data = data
        self.shape = np.shape(self.beam_profile_data)
        self.color_resolution = color_resolution

    def slice_horizontally(self, h_min, h_max):
        # t = time.time()
        data = self.beam_profile_data[:, :, h_min:h_max]
        # print('Horizontal slice timing: {}'.format(time.time() - t))
        return BeamProfilesPipeline(data=data)

    def slice_vertically(self, v_min, v_max):
        # t = time.time()
        data = self.beam_profile_data[:, v_min:v_max, :]
        # print('Vertical slice timing: {}'.format(time.time() - t))
        return BeamProfilesPipeline(data=data)

    def change_color_resolution(self, new_resolution):
        # t = time.time()
        data = background_remove_tools.change_color_resolution(self.beam_profile_data,
                                                               new_resolution,
                                                               self.color_resolution)
        color_resolution = new_resolution
        # print('Changing color resolution time: {}'.format(time.time() - t))
        return BeamProfilesPipeline(data, color_resolution)

    def remove_background_by_intensity_fraction(self, cut_off_level):
        # t = time.time()
        data = background_remove_tools.remove_background_by_intensity_fraction(self.beam_profile_data, cut_off_level)
        # print('Background remove timing: {}'.format(time.time() - t))
        return BeamProfilesPipeline(data, self.color_resolution)

    def remove_background(self, number_of_lowest_colors=2, masking_color_resolution=7):
        data = background_remove_tools.remove_background(self.beam_profile_data,
                                                         initial_color_resolution=self.color_resolution,
                                                         processing_color_resolution=masking_color_resolution,
                                                         number_of_lowest_to_cut=number_of_lowest_colors)
        return BeamProfilesPipeline(data, self.color_resolution)

    def opening(self):
        # t = time.time()
        data = background_remove_tools.grayscale_opening(self.beam_profile_data)
        # print('Opening timing: {}'.format(time.time() - t))
        return BeamProfilesPipeline(data, self.color_resolution)

    def shift_to_center_of_mass(self):
        # t = time.time()
        data = image_shifting.shift_com_to_geometric(self.beam_profile_data)
        # print('Shifting to com timing: {}'.format(time.time() - t))
        return BeamProfilesPipeline(data, self.color_resolution)

    def get_rounded_beam_profiles(self):
        return np.round(self.beam_profile_data)

    def rescale_images(self, horizontal_scale=1.1):
        # t = time.time()
        data = skimage.transform.rescale(self.beam_profile_data, scale=(1, 1, horizontal_scale), multichannel=False)
        shape_corrected_data = data[:, :, :self.beam_profile_data.shape[-1]]
        # print('Rescale timing: {}'.format(time.time() - t))
        return BeamProfilesPipeline(shape_corrected_data, color_resolution=self.color_resolution)

    def shift_to_highest_intensity(self, fraction):
        data = image_shifting.shift_highest_intensity_to_geometric(self.beam_profile_data, fraction=fraction)
        return BeamProfilesPipeline(data, self.color_resolution)


    def standardize(self):
        pass