#!/bin/bash

source ./init.sh

cd platolocorestapi/src

python3 waitress_server.py
