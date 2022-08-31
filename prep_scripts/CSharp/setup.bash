#!/usr/bin/env bash

function prep_directory() {
    if [ ! -d "$1" ]; then
        echo "$1 does not exist, bailing out"
        return
    fi
    pushd "$1" || return
    dotnet new console --output . --name tmp -all --language C#
    dotnet restore
    popd || return
}

tests=('binary-trees' 'chameneos-redux' 'fannkuch-redux' 'fasta' 'k-nucleotide'
         'mandelbrot' 'n-body' 'pidigits' 'regex-redux' 'reverse-complement' 'spectral-norm'
         'thread-ring')

function prep_all() {
    for test_dir in "${tests[@]}"; do
        prep_directory "$test_dir"
    done
}

if [ "$(basename "$(pwd)")" = "CSharp" ]; then
    prep_all
else
    echo "Expected to be in a directory named 'CSharp', but found $(pwd)"
fi