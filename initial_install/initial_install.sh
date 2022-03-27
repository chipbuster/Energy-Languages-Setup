#!/usr/bin/env bash

if [[ $EUID -ne 0 ]]; then
   echo "This script must be run as root" 
   exit 1
fi

# If we are on a 16.10 release (running for legacy reproducibility), we need to
# do some things to be able to access repositories.
function perform_1610_setup(){
    sudo sed -i -re 's/([a-z]{2}\.)?archive.ubuntu.com|security.ubuntu.com/old-releases.ubuntu.com/g' /etc/apt/sources.list
    sudo apt-get update --assume-yes
    sudo apt-get dist-upgrade --assume-yes

    # Makedeb requires a newer version of bash than is present on Ubuntu 16.10.
    # Compile a copy of bash 5.1 so that makedeb will work.
    tar xf bash-5.1.16.tar.gz
    pushd bash-5.1.16 || exit 1
    ./configure
    make -j "$(nproc)"
    sudo make install
    popd || exit 1

    # Makedeb also requires a modern version of bsdtar (repo version is too old)
    # Compile and install that as well. Installing to default (/usr/local/) is
    # fine since makedeb will pick up on that directory before /usr/bin
    tar xf libarchive-3.6.0.tar.xz
    pushd libarchive-3.6.0 || exit 1
    ./configure
    make -j "$(nproc)"
    sudo make install
    popd || exit 1
}

function perform_general_setup(){
    # Install general prerequisites for what we're about to do
    sudo apt install --assume-yes vim git curl wget build-essential python3-pip python3 valgrind asciidoctor\
                                  binutils fakeroot file libarchive-tools lsb-release python3-apt bsdtar zstd

    # Install makedeb to ease management of packages
    tar xf v11.0.1-1-stable.tar.gz
    pushd makedeb-11.0.1-1-stable/ || exit 1
    make prepare
    sudo make package
    popd || exit 1
}

if [[ ! -f "/etc/os-release" ]]; then
    echo "ERROR: /etc/os-release not found. Refusing to continue: this is probably not an Ubuntu system."
    exit 1
else
    SCRIPT_DIR="$( cd -- "$( dirname -- "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )"
    cd "$SCRIPT_DIR" || exit 1
    source "/etc/os-release"
    if [[ $NAME != "Ubuntu" ]]; then
        echo "ERROR: This script is only meant to be run on Ubuntu, but this is $NAME."
    fi
    if [[ $VERSION_ID == "16.10" ]]; then
        echo "Found Ubuntu 16.10: performing 16.10 setup."
        perform_1610_setup
    else
        echo "Found Ubuntu $VERSION_ID: not performing 16.10-specific setup."
    fi

    echo "Installing general prerequisites."
    perform_general_setup
    echo "General setup complete. You are now ready to install the language runtimes."
fi
