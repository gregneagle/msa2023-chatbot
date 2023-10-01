#!/bin/bash

SOURCE=${BASH_SOURCE[0]}
THISDIR=$(dirname "${SOURCE}")
PYTHON="${THISDIR}/Python.framework/Versions/Current/bin/python3"
cd "$THISDIR"
xattr -dr com.apple.quarantine Python.framework
${PYTHON} ./local_chatbot.py