#!/bin/bash

# run this from the root of the repository directory to post the package to
# PyPI

[[ -d dist_venv ]] || virtualenv --python=python3 dist_venv
source dist_venv/bin/activate

mkdir -p dist
rm dist/*

python setup.py sdist bdist_wheel
twine upload dist/*
