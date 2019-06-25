# LIBCAISE
Learning Interpretable Behavioral Components from Assembly Instructions of Software Executables

This repo contains all work and code associated with the LIBCAISE system. All python code should be cross-platform, but the shell scripts have only been tested on Ubuntu and so will probably only work on Linux. All searching and sorting programs were taken from geeksforgeeks.org as c++ files. 

## Dependencies:
* Python3
* guidedlda
* numpy
* gensim
* scipy
* pickle
* matplotlib
* pandas
* hlda
* nltk

All dependencies should be installable via pip, and most may already be installed if using Anaconda.

## Usage:
* `python run_lda.py` runs lda on the dataset listed in the file
* `python run_hlda.py` works similarly but for hierarchical LDA
* `python cluster_asm.py` will generate clusters for the files listed in the directory provided. Note that the cutting point needs to be manually defined by the user.
* `python convert_to_uci.py` will convert the data to the UCI format utilized by LightLDA
* `./get_static.sh` will collect the static assemblies of the binary files in the `/bin/` directory
* `./get_dynamic.sh` will collect the dynamic assemblies of the binary files in the `bin/` directory

In addition, `read_light_lda_files.py` in the `util` directory can be run to visualize the results from lightLDA in a manner similar to guidedlda.

## LightLDA
The files `convert_to_uci.pi` and `read_light_lda_files.py` are the files to be utilized with LightLDA. Installation instructions for LightLDA can be found here: https://github.com/microsoft/LightLDA

Note that you may encounter some issues during the installation of it and its dependencies, but the issue list for LightLDA should help with that.

Once LightLDA is installed and built, one must use the `convert_to_uci.py` file to generate files in the correct format used by LightLDA (if you already have files in the UCI format then you shoudl be fine.

Once you have files in the UCI format, you'll need to transfer the files to an appropriate place in the LightLDA directory. Once it's finished, LightLDA will generate some files containing probability distribution tables, which can then be copied back over to the libcaise directory and read using the `read_light_lda_files.py` file. This file will display results similarly to the `run_lda.py` file.

LightLDA is described as both multi-threaded and parallelizable, but I haven't tested running it on multiple computers, so I can't attest to how that would work, but there are instructions included in the LightLDA repo
