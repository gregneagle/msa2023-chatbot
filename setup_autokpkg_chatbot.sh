#!/bin/bash

SOURCE=${BASH_SOURCE[0]}
THISDIR=$(dirname "${SOURCE}")
cd "$THISDIR"
rm -r documents/*
if [ ! -d index_storage ] ; then
    mkdir index_storage
else
    rm -r index_storage/*
fi
cp -R example_docs/autopkg/* documents/