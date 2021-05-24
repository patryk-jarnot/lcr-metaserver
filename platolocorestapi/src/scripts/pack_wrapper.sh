#!/bin/bash

python increase_version.py

if [ -f output/wrapper ]; then
    rm output/wrapper
fi

cd ..

ln -s src/__main__.py __main__.py
zip -r wrapper.zip src __main__.py
rm __main__.py

if [ ! -d output ]; then
    mkdir output
fi

mv wrapper.zip scripts/output/wrapper

