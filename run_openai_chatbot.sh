#!/bin/bash

SOURCE=${BASH_SOURCE[0]}
THISDIR=$(dirname "${SOURCE}")
PYTHON="${THISDIR}/Python.framework/Versions/Current/bin/python3"
cd "$THISDIR"
${PYTHON} ./openai_chatbot.py