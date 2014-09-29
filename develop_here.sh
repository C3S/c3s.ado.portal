#!/bin/bash
#
# you can use this script to start hacking on c3s.ado.portal.
#

# use a virtual python environment,
# so installed packages don't go to your system python
virtualenv env

# install pyramid and cornice
./env/bin/pip install pyramid cornice

# create template project from scaffold
# (this is a one off: you need this only once! created files are versioned)
#./env/bin/pcreate -t cornice -t alchemy ../c3s.ado.portal

# set it up for development; pulls in the dependencies
./env/bin/python setup.py develop

# start the app
# * the reload option will restart the app every time a source file changes
./env/bin/pserve development.ini --reload
