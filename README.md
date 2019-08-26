# DESY_photon_pulse_property_predictor

## Overview

The main purpose of this code is the analysis of beam profiles taken at DESY's FLASH 2 facility. There were two distinct stages to the project:

1. Determining the Gaussianeity of the profiles using computer vision and machine learning.
2. Reduction of dimensions for analysis of the beam profiles in terms of machine settings, Gaussianeity and other labels.

## Subdivision

The project can be subdivided into:

1. An import tool for loading the profiles from .h5 files.
2. A tool for Metadata creation and saving for the imported profiles.
3. A tool for Gaussian - higher order labeling of the profiles using Computer Vision.
4. A Convolutional Neural Network for Gaussian - higher order classification.
5. An Autoencoder for dimensionality reduction of the profiles.
6. A PCA algorithm to get an orthogonal 2D space to represent the profiles.
7. Imaging tools to view the profiles.


## Usage

To use please make sure that all the packages from the requirements.txt file are installed.

