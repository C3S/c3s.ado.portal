#!/bin/bash

#
# script for jenkins to run the tests
#

# make a virtual python environment
virtualenv env

# set up for development, get dependencies
./env/bin/python setup.py develop

# run the tests
./env/bin/nosetests --cover-html --with-xunit

# for pyflakes
find c3sadoportal -regex '.*.py' ! -regex '.*tests.*'|egrep -v '^./tests/'|xargs env/bin/pyflakes  > pyflakes.log || :
# for pylint
rm -f pylint.log
for f in `find c3sadoportal -regex '.*.py' ! -regex '.*tests.*'|egrep -v '^./tests/'`; do
env/bin/pylint --output-format=parseable --reports=y $f >> pylint.log
done || :
