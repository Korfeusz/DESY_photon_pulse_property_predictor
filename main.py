import file_tools
import h5py
import matplotlib.pyplot as plt
import numpy as np

if __name__ == '__main__':
    image_number = 20
    run_number = 3
    beam_profile = file_tools.get_one_beam_profile(run_number=run_number, profile_number=image_number)

    desired_color_bits = 63
    initial_color_bits = 4095
    horizontal_slice = (94, 350)
    vertical_slice = (94, 350)
    current_beam_profile = (beam_profile[vertical_slice[0]:vertical_slice[1],
                            horizontal_slice[0]:horizontal_slice[1]]
                            / initial_color_bits * desired_color_bits).astype(np.int)

    plt.imsave('save_test.png',
               current_beam_profile,
               cmap=plt.cm.jet)
    print(current_beam_profile.max())
