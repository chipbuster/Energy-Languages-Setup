FROM ubuntu:16.10

RUN useradd -ms /bin/bash user
RUN passwd -d user
USER user
WORKDIR /home/user

USER root

# Running the initial install script causes some horrendous issues with disk 
# space usage and repeatability of the build when doing incremental changes.
# For now, substitute the initial install procedures with an expansion of the
# shell scripts so that we can actually do incremental work. TODO: Replace these
# with the primary scripts later.

#### Initial Setup Expansion

# 16.10-specific: Point apt to the correct mirrors and grab a few essentials
RUN sed -i -re 's/([a-z]{2}\.)?archive.ubuntu.com|security.ubuntu.com/old-releases.ubuntu.com/g' /etc/apt/sources.list
RUN apt-get update --assume-yes
RUN apt-get dist-upgrade --assume-yes
RUN apt-get install --assume-yes xz-utils build-essential sudo

COPY --chown=user preinstall_setup preinstall_setup

# 16.10-specific: compile a copy of bash 5.1 for makedeb
WORKDIR /home/user/preinstall_setup/
RUN tar xf bash-5.1.16.tar.gz
WORKDIR /home/user/preinstall_setup/bash-5.1.16
RUN ./configure && make -j16 && make install

# 16.10-specific: compile a copy of bsdtar for makedeb
WORKDIR /home/user/preinstall_setup/
RUN tar xf libarchive-3.6.0.tar.xz
WORKDIR /home/user/preinstall_setup/libarchive-3.6.0
RUN ./configure && make -j16 && make install

# Additional setup for all ubuntu versions
RUN apt-get install --assume-yes vim git curl wget build-essential python3-pip valgrind asciidoctor\
            binutils fakeroot file libarchive-tools lsb-release python3-apt bsdtar zstd\
            cmake jq sudo python3 python

# Install makedeb
WORKDIR /home/user/preinstall_setup/makedeb-11.0.1-1-stable
RUN CURRENT_VERSION=11.0.1 TARGET=apt RELEASE=alpha make prepare && make package
RUN echo "MAKEFLAGS=-j32" | tee -a /etc/makepkg.conf
#### End Initial Setup

RUN echo "user ALL=(ALL) NOPASSWD: ALL" >> /etc/sudoers
USER user

WORKDIR /home/user/
COPY --chown=user /pkgbuilds/ ./pkgbuilds
COPY --chown=user gen_deb_file.sh gen_deb_file.sh

# This line should be uncommented if you need to download all the files for the
# first time.
#RUN python3 download_files.py

WORKDIR /home/user
RUN mkdir debs

# Build deps/langs. Ordered so that the more problematic ones are built last for
# maximum reusability
RUN bash gen_deb_file.sh ./pkgbuilds/Ada
RUN bash gen_deb_file.sh ./pkgbuilds/C
RUN bash gen_deb_file.sh ./pkgbuilds/C++
RUN bash gen_deb_file.sh ./pkgbuilds/Chapel
RUN bash gen_deb_file.sh ./pkgbuilds/Dart
RUN bash gen_deb_file.sh ./pkgbuilds/Dotnet
RUN bash gen_deb_file.sh ./pkgbuilds/Erlang
RUN bash gen_deb_file.sh ./pkgbuilds/Fortran
RUN bash gen_deb_file.sh ./pkgbuilds/Go
RUN bash gen_deb_file.sh ./pkgbuilds/Hack
RUN bash gen_deb_file.sh ./pkgbuilds/Haskell
RUN bash gen_deb_file.sh ./pkgbuilds/Java
RUN bash gen_deb_file.sh ./pkgbuilds/JavaScript
RUN bash gen_deb_file.sh ./pkgbuilds/JRuby
RUN bash gen_deb_file.sh ./pkgbuilds/Lisp
RUN bash gen_deb_file.sh ./pkgbuilds/Lua
RUN bash gen_deb_file.sh ./pkgbuilds/OCaml
RUN bash gen_deb_file.sh ./pkgbuilds/Pascal
RUN bash gen_deb_file.sh ./pkgbuilds/Perl
RUN bash gen_deb_file.sh ./pkgbuilds/PHP
RUN bash gen_deb_file.sh ./pkgbuilds/Python
RUN bash gen_deb_file.sh ./pkgbuilds/Racket
RUN bash gen_deb_file.sh ./pkgbuilds/Ruby
RUN bash gen_deb_file.sh ./pkgbuilds/Rust
RUN bash gen_deb_file.sh ./pkgbuilds/Swift

USER root
RUN apt-get install -f  ./debs/*

# TypeScript needs to be installed after JavaScript's npm dependency
USER user
RUN bash gen_deb_file.sh ./pkgbuilds/TypeScript
USER root
RUN apt-get install -f ./debs/energy-languages-typescript_2.3.1-1_amd64.deb
USER user

# TypeScript relies on being able to find node: add this to the PATH to avoid sadness
ENV PATH="${PATH}:/usr/local/src/node-v7.9.0-linux-x64/bin"

# Let's install prerequisites
WORKDIR /home/user
COPY --chown=user /prerequisites/ ./prerequisites
RUN bash gen_deb_file.sh ./prerequisites/aptreqs
RUN bash gen_deb_file.sh ./prerequisites/icu52

USER root
RUN apt-get install --assume-yes -f ./debs/*
USER user

# Install the benchmarking code
RUN git clone https://github.com/greensoftwarelab/Energy-Languages.git
# Remove languages which were not present in the original benchmarks
RUN rm -rf Energy-Languages/Julia
RUN rm -rf Energy-Languages/Smalltalk

ENTRYPOINT ["bash", "-l"]