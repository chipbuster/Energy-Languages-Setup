# Language Runtime/Compiler Downloads

This folder contains the downloading + validation code for language runtimes for
the 2016 version of the paper.

Ideally, we would be able to download these as part of the installation procedure.
However, due to SSL certificate expiration in the cert store, Ubuntu 16.10 has
slowly been able to access less and less of the internet without disabling
host verification. In addition, as many of these runtimes are older, it's not
clear that they will be available in the future.

For this reason, there are two ways provided to acquire these runtimes:

1. By using the provided script to download and verify the runtimes (from a
   newer OS, which can then be transferred to the Ubuntu 16.10 system)
2. By using Git LFS

If possible, please use the former, as it places less stress on the Git
repository.
