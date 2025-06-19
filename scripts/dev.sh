#!/bin/bash

source ./scripts/setup.sh
watchmedo auto-restart --pattern "*.py" --recursive --signal SIGTERM python ./qserver/main.py -- -v $@