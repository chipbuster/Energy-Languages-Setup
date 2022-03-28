#!/bin/bash

SCRIPT_DIR="$( cd -- "$( dirname -- "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )"
SCRIPT_DIR="$(realpath "$SCRIPT_DIR")"

pushd "${SCRIPT_DIR}/preinstall_setup" || exit 1

sudo bash initial_install.sh
python3 download_files.py

popd || exit 1

# Just build packages for now.
debdir="${SCRIPT_DIR}/debs"
mkdir -p "${debdir}"
for lang in "${SCRIPT_DIR}/pkgbuilds/"*; do
    if [[ -d "$lang" ]]; then
        pushd "$lang" || exit 1
        if ls ./*.deb &>/dev/null; then
            makedeb -s
            mv ./*.deb "${debdir}"
        fi
        popd || exit 1
    fi
done

for deb in "${debdir}/"*; do
    sudo apt-get install -f --yes "$deb"
done