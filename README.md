# README


This is our space trader game for CS2340.


Please see this tutorial see what is going on:
https://blog.miguelgrinberg.com/post/the-flask-mega-tutorial-part-ii-templates

# Get Started

Install anaconda and run:
    conda env create -f environment.yml
    # This will setup the environment and install the required dependencies
    make setup
    # Exports Flask runner to bash

For every session:
    conda activate cs2340
    # Starts virtual environment
    flask run
    # Launches flask server


# Makefile

The purpose of the Makefile is to run project wide scripts such as setup, download, and clean.
To use a script run:
    make {script alias}

# Anaconda Environment

The purpose of using an Anaconda environment is to keep package management clean and simple.
No need for pycaches everywhere.
To get started:
    Install Anaconda Command Line Installer
    https://www.anaconda.com/distribution/#download-section
    Run the shell script with bash.

To activate conda environment from yml file run:
    conda env create -f environment.yml

Then activate the environment:
    conda activate {environment name}

To deactivate:
    conda deactivate

To install dependencies use:
    conda install {dependency name}

Make sure to add any new dependencies to the yml file.
