import file_tools
import h5py
import matplotlib.pyplot as plt
from matplotlib import cm

if __name__ == '__main__':
    current_run_path = file_tools.get_run_path(run_number=8)
    with h5py.File(current_run_path, 'r') as current_run:
        beam_profiles = file_tools.get_beam_profiles(run=current_run)
        plt.imsave('save_test.png', beam_profiles[400, 94:350, 94:350], cmap=cm.jet)

