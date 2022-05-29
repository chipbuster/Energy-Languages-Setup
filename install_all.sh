#!/bin/bash

SCRIPT_DIR="$( cd -- "$( dirname -- "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )"
SCRIPT_DIR="$(realpath "$SCRIPT_DIR")"

pushd "${SCRIPT_DIR}/preinstall_setup" || exit 1

bash initial_install.sh
python3 download_files.py

popd || exit 1
