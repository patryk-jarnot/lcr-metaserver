#!/bin/bash

cd platolocoui

if ! screen -list | grep -q "plato_ui"; then
    screen -dmS plato_ui npm start
fi


cd ..
source ./init.sh

cd platolocorestapi/src

if ! screen -list | grep -q "plato_rest"; then
    screen -dmS plato_rest python3 __main__.py
fi
