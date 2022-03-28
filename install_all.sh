#!/bin/bash

SCRIPT_DIR="$( cd -- "$( dirname -- "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )"

pushd "${SCRIPT_DIR}/preinstall_setup" || exit 1

sudo bash initial_install.sh
python3 download_files.py

popd || exit 1

# Just build packages for now.
for lang in "${SCRIPT_DIR}/pkgbuilds/"*; do
    if [[ -d "$lang" ]]; then
        pushd "$lang" || exit 1
        makedeb -s
        popd || exit 1
    fi
done

# Run installation
for lang in "${SCRIPT_DIR}/pkgbuilds/"*; do
    if [[ -d "$lang" ]]; then
        pushd "$lang" || exit 1
        sudo apt-get install --force --yes ./*.deb
        popd || exit 1
    fi
done