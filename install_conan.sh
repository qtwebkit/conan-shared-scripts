#!/bin/sh
BASEDIR=$(dirname "$0")
#pip3 install -r "$BASEDIR/conan_requirements.txt"
pip3 install conan_package_tools==0.34.2 conan==1.29.0
pip3 freeze
conan user
