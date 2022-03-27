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
    sudo apt-get upgrade --assume-yes
    sudo apt-get install --assume-yes wget curl

    # Makedeb requires a newer version of bash than is present on Ubuntu 16.10.
    # Download and compile a copy of bash 5.1 so that makedeb will work.
    curl --location --remote-name --insecure http://ftp.gnu.org/gnu/bash/bash-5.1.16.tar.gz
    if ! echo "5bac17218d3911834520dad13cd1f85ab944e1c09ae1aba55906be1f8192f558 bash-5.1.16.tar.gz" | sha256sum --check; then
      echo "Cannot validate bash download: sha256 checksum failed"
      exit 1
    fi
    tar xf bash-5.1.16.tar.gz
    cd bash-5.1.16 || exit 1
    ./configure
    make -j "$(nproc)"
    sudo make install
}

function perform_general_setup(){
    # Install general prerequisites for what we're about to do
    sudo apt install --assume-yes vim git curl wget build-essential python3-pip python3 valgrind asciidoctor\
                                  binutils fakeroot file libarchive-tools lsb-release python3-apt zstd
      

    # Install makedeb to ease management of packages
    curl --location --remote-name --insecure https://github.com/makedeb/makedeb/archive/refs/tags/v11.0.1-1-stable.tar.gz

    if ! echo "44844c2fbdc0fc70203f6cefe65ae6badd240b841f77ba6e4d28c884e0c4c28a  v11.0.1-1-stable.tar.gz" | sha256sum --check; then
        echo "Cannot validate makedeb download: sha256 checksum failed"
        exit 1
    fi
    tar xf v11.0.1-1-stable.tar.gz
    cd makedeb-11.0.1-1-stable/ || exit 1
    make prepare
    sudo make package
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
