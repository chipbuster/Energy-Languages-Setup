# Initial Installer

The `initial_install.sh` script sets up the initial installation for the rest
of the language installers, as well as taking care of issues in Ubuntu 16.10.
It must be run as root, since it installs packages.

The steps it takes are:

- Check that the installation is Ubuntu. If it is not, script does nothing.
- If the version is Ubuntu 16.10, it further does setup by:
  - [Change mirrors to point at old-releases.ubuntu.com](https://askubuntu.com/questions/91815/how-to-install-software-or-upgrade-from-an-old-unsupported-release)
  - Install bash-5.1.16 for use with `makedeb` (since the default bash on 16.10
    is too old to support `makedeb`).
  - Install libarchive 3.6.0 for use with `makedeb` (since the default bsdtar
    on 16.10 is too old to support `makedeb`).
- Install a custom-patched version of `makedeb` that replaces hardcoded `zstd`
  extensions with hardcoded `gz` extensions. This does not harm newer versions
  of Ubuntu, but is required for compatibility on older versions of Ubuntu. This
  custom version also removes certain flags which cause issues with older tools.

NOTE: this version of makedeb is pretty busted, because makedeb was written to
run on Ubuntu 20.04 and we're taking it back to Ubuntu 16.10. The version here
has been patched

# File Downloader

The `download_files.py` script downloads the files needed by makedeb to install
the

1. By using the provided script to download and verify the runtimes
2. By downloading a tarball of the runtimes from the link below.

## Obtain Files by Running Script

In order to obtain the files by direct download, run `python3 download_files.py`.
This will download and checksum the necessary files into the appropriate pkgbuild
directory (`../pkgbuilds/<LANGNAME>` relative to this directory.)

## Obtain files by download

If you are unable to use the above method, you can download a `.tar` file
containing all of the language runtimes from the link below:

https://www.dropbox.com/s/97ggu2vo51qw9z6/all_language_runtimes.tar?dl=0

Note that short of manually checksumming all the files yourself and comparing
them to what is present in `download_files.py`, there is not currently a way to
verify the integrity of the files if using this method.
