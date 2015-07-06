#!/bin/bash

#echo "Building both Windows and Linux executables."
#wine pyinstaller -F main-win.spec
pyinstaller -F main-linux.spec
