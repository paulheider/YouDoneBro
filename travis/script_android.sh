#!/bin/bash
# Android specific Travis script

# exits on fail
set -e

sudo -H pip install --upgrade cython==0.21
sudo -H pip install --upgrade buildozer==0.32
./travis/buildozer_android.sh
