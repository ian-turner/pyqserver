#!/bin/bash

# kills all processes using port 1901 (sometimes python procs can hang on)
kill `lsof -i :1901 | awk '{print $2}' | tail +2`