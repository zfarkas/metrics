#!/bin/bash

cd "$( dirname "${BASH_SOURCE[0]}" )"
source ./bin/activate
python reg_test.py
