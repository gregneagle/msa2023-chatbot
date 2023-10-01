#!/bin/bash

SOURCE=${BASH_SOURCE[0]}
THISDIR=$(dirname "${SOURCE}")
PYTHON="${THISDIR}/Python.framework/Versions/Current/bin/python3"
cd "$THISDIR"
xattr -dr com.apple.quarantine Python.framework
if [ -e "documents/README.txt" ] ;  then
    echo "****** Did you copy documents into the documents folder, and did you remove the default README.txt? ********"
    sleep 2
fi
${PYTHON} ./local_chatbot.py