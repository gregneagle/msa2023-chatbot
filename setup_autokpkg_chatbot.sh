#!/bin/bash

SOURCE=${BASH_SOURCE[0]}
THISDIR=$(dirname "${SOURCE}")
cd "$THISDIR"
rm -r documents/*
rm -r index_storage/*
cp -R example_docs/autopkg/* documents/