#!/bin/bash

#echo "Building both Windows and Linux executables."
#wine pyinstaller -F main.spec
pyinstaller -F main.spec
