import file_tools
import h5py
import matplotlib.pyplot as plt

if __name__ == '__main__':
    current_run_path = file_tools.get_run_path(1)
    with h5py.File(current_run_path, 'r') as current_run:
        beam_profiles = file_tools.get_beam_profiles(current_run)
        plt.imsave('save_test.png', beam_profiles[499, :, :])
