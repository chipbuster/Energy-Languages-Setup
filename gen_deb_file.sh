#!/bin/bash

SCRIPT_DIR=$( cd -- "$( dirname -- "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )
debdir="$SCRIPT_DIR/debs"

path="$1"
pushd "$path"
makedeb -s
mv ./*.deb "$debdir"