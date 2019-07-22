import file_tools
import h5py


if __name__ == '__main__':
    current_run_path = file_tools.get_run_path(0)
    with h5py.File(current_run_path, 'r') as current_run:
        beam_profiles = file_tools.get_beam_profiles(current_run)
        print(beam_profiles.size)
