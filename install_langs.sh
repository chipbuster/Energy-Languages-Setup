#!/bin/bash

set -x

SCRIPT_DIR="$( cd -- "$( dirname -- "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )"
SCRIPT_DIR="$(realpath "$SCRIPT_DIR")"

# Just build packages for now.
debdir="${SCRIPT_DIR}/debs"
mkdir -p "${debdir}"
for lang in "${SCRIPT_DIR}/pkgbuilds/"*; do
    if [[ -d "$lang" ]]; then
        pushd "$lang" || exit 1
        makedeb -s
        mv ./*.deb "${debdir}"
        popd || exit 1
    fi
done