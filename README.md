# LIBCAISE
Learning Interpretable Behavioral Components from Assembly Instructions of Software Executables

This repo contains all work and code associated with the LIBCAISE system. All python code should be cross-platform, but the shell scripts have only been tested on Ubuntu and so will probably only work on Linux. All searching and sorting programs were taken from geeksforgeeks.org as c++ files. 

Dependencies:
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

Usage:
* `python run_lda.py` runs lda on the dataset listed in the file
* `python run_hlda.py` works similarly but for hierarchical LDA
* `python cluster_asm.py` will generate clusters for the files listed in the directory provided. Note that the cutting point needs to be manually defined by the user.
* `python convert_to_uci.py` will convert the data to the UCI format utilized by LightLDA
* `./get_static.sh` will collect the static assemblies of the binary files in the `/bin/` directory
* `./get_dynamic.sh` will collect the dynamic assemblies of the binary files in the `bin/` directory

In addition, `read_light_lda_files.py` in the `util` directory can be run to visualize the results from lightLDA in a manner similar to guidedlda.
