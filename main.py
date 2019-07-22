import file_tools
import h5py

if __name__ == '__main__':
    current_run = file_tools.get_run_path(0)
    print(current_run)
    run_file = h5py.File(current_run, 'r')

    run_file.close()