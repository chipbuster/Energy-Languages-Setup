# Language Runtime/Compiler Downloads

This folder contains the downloading + validation code for language runtimes for
the 2017 version of the paper. It downloads all the tarballs needed by the

1. By using the provided script to download and verify the runtimes
2. By downloading a tarball of the runtimes from the link below.

## Obtain Files by Running Script

In order to obtain the files by direct download, run `python3 download_files.py`.
This will download and checksum the necessary files into the `downloads` folder
in this directory.

It may be possible to run this script from within a copy of Ubuntu 16.10.
However, due to issues with aging SSL certificate stores and host verification,
it may not be possible to successfully download the files successfully from
Ubuntu 16.10. If this is the case, I recommend downloading the files from a
modern OS, and then copying this entire repository over to the target system
on a USB stick (its size should not exceed 1GiB).

## Obtain files by download

If you are unable to use the above method, you can download a `.tar` file
containing all of the language runtimes from the link below:

https://www.dropbox.com/s/97ggu2vo51qw9z6/all_language_runtimes.tar?dl=0

Note that short of manually checksumming all the files yourself and comparing
them to what is present in `download_files.py`, there is not currently a way to
verify the integrity of the language files.
