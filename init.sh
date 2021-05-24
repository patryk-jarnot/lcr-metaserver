#!/usr/bin/env bash
echo "usage: source ./init.sh"
echo $(pwd)
export PYTHONPATH=$(pwd)
if [[ -f venv/bin/activate ]]; then
    source venv/bin/activate
fi
