# DESY_photon_pulse_property_predictor

## Overview

The main purpose of this code is the analysis of beam profiles taken at DESY's FLASH 2 facility. There were two distinct stages to the project:

1. Determining the Gaussianeity of the profiles using computer vision and machine learning.
2. Reduction of dimensions for analysis of the beam profiles in terms of machine settings, Gaussianeity and other labels.

## Division

The project can be divided into:

1. An import tool for loading the profiles from .h5 files.
2. A tool for Metadata creation and saving for the imported profiles.
3. A tool for Gaussian - higher order labeling of the profiles using Computer Vision.
4. A Convolutional Neural Network for Gaussian - higher order classification.
5. An Autoencoder for dimensionality reduction of the profiles.
6. A PCA algorithm to get an orthogonal 2D space to represent the profiles.
7. Imaging tools to view the profiles.


## Usage

To use please make sure that all the packages from the requirements.txt file are installed. Using this project consists of the sequential use of the tools, each of which creates a permanent record on the device to be used by the next step. This way the next step is independent of the previous one and changing a parameter does not mean re-running everyhing.

### Importing
First the constants.py file has to be modified and the proper path to the beam profiles on the machine "experiment_data_directory" and the path to the profiles inside the hdf file  "beam_profiles_path" have to be supplied. The "run_inputs_save_file" variable is the name of the .json metadata file, where each profile will get its own entry and all subsequently created information about the profile will be stored. The "run_input_file_template" is the location of the settings for each run, where runs are labelled by integers and will be formatted into the template. The "run_numbers" list specifies which runs should be processed. The beam profiles after preprocessing will be stored in a numpy format. Preprocessing constitutes cropping, removing the backround, rescaling and shifting the image to the center of the peak. The last operation can be done either by shifting to the highest intensity or to the center of mass of the image. 
An example run input file is here:
#### Example run input json:
 
 
 {
    "experiment_name": "0", # The name of the current test run
    "profiles_range": 0, # Supplying a list would just import the list, any other value means importing all profiles
    "slice": { # Cropping parameters in pixels
        "horizontal": {
            "min": 105,
            "max": 364
        },
        "vertical": {
            "min": 90,
            "max": 349
        }
    },
    "final_color_resolution": 63, # The final number of distinct values to be encoded on the image
    "run_number": 2, # The beam run number
    "background_cut_off": 0.6, # The fraction of the maximum pixel value at which the backround is cut off, or the fraction of the maximal energy of the beam
    "horizontal_scaling_factor": 1.2, # The factor by which the image should be downscaled
    "shifting": { # The parameters used for shifting the beam peak to the center
        "type": "highest_intensity", # The type of shifting, the other one is "center_of_mass"
        "fraction": 0.8
    }
}
### Metadata creation

### Labeling

### CNN

### Autoencoder

### PCA

### Imaging tools

## Example metadata json:
``` json
 "0_1": {
    "address": {
      "run": 0,
      "profile_number": 1
    },
    "corrupted": false,
    "circularity_index": {
      "run_name_0_masking_settings_10_2": {
        "type": "area_perimeter",
        "settings": {
          "ring_thickness": 10,
          "number_of_tests": 2
        },
        "pipeline_settings_name": "0",
        "value": 0.294592246161292
      },
      "run_name_0_area_perimeter_settings_3_5_7": {
        "type": "area_perimeter",
        "settings": [
          0.3,
          0.5,
          0.7
        ],
        "pipeline_settings_name": "0",
        "value": 0.7557831967788516
      }
    },
    "label": {
      "run_name_0_masking_settings_10_2": {
        "value": 0,
        "threshold": 0.19
      },
      "run_name_0_area_perimeter_settings_3_5_7": {
        "value": 0,
        "threshold": 0.45
      },
      "experimental_combo": {
        "value": 0
      },
      "combination_label": {
        "value": 0
      }
    },
    "train_test": "unused",
    "autoencoder": {
      "train_test": "train",
      "model_file": "model/autoencoder_tst_1.h5",
      "code_file": "/beegfs/desy/user/brockhul/autoencoder_codes/autoencoder_tst_1.npy",
      "encoder_file": "model/autoencoder_tst_1_encoder.h5",
      "code_index": 1
    }
  },
 ```
 
