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

To use please make sure that all the packages from the requirements.txt file are installed.

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
 ## Example run input json:
 
 ``` json
 {
    "experiment_name": "0",
    "profiles_range": 0,
    "slice": {
        "horizontal": {
            "min": 105,
            "max": 364
        },
        "vertical": {
            "min": 90,
            "max": 349
        }
    },
    "final_color_resolution": 63,
    "run_number": 2,
    "background_cut_off": 0.6,
    "horizontal_scaling_factor": 1.2,
    "shifting": {
        "type": "highest_intensity",
        "fraction": 0.8
    }
}
 ```