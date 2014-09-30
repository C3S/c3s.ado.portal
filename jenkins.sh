#!/bin/bash

#
# script for jenkins to run the tests
#

# make a virtual python environment
virtualenv env

# set up for development, get dependencies
./env/bin/python setup.py develop

# run the tests
./env/bin/nosetests
