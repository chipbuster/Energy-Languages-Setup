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
  of Ubuntu, but is required for compatibility on older versions of Ubuntu.
