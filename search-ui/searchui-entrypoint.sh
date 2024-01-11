#!/bin/bash

set -x

source ~/.bashrc

echo "PWD: $PWD"

cd /usr/src/app/app-search-reference-ui-react-main

echo "PWD: $PWD"

# Instructions for user
echo "============================================================================================="
echo "After seeing the message 'webpack 5.89.0 compiled ... in ____ ms',
pls proceed to check on the front end by accessing http://localhost:3000 in your browser."
echo "============================================================================================="

yarn start