import ssl
import urllib.request
import os
import hashlib

# Get the path to the pkgbuilds directory
filepath = os.path.abspath(__file__)
pkgbuild_dir = os.path.join(os.path.dirname(os.path.dirname(filepath)), "pkgbuilds")

# Spoof a curl client so that some websites don't immediately 403 us
default_header = {"user-agent": "curl/7.82.0", "accept": "*/*"}

# Define a context where we disable host checking for SSL certificates. Host
# checking fails on Ubuntu 16.10 and is irrelevant for this script because
# we validate the SHA256 hash of the file anyways.
default_ssl_ctx = ssl.create_default_context()
default_ssl_ctx.check_hostname = False
default_ssl_ctx.verify_mode = ssl.CERT_NONE

# Taken from https://stackoverflow.com/a/44873382/2914377
def sha256sum(filename):
    h = hashlib.sha256()
    b = bytearray(16 * 4096)
    mv = memoryview(b)
    with open(filename, "rb", buffering=0) as f:
        for n in iter(lambda: f.readinto(mv), 0):
            h.update(mv[:n])
    return h.hexdigest()


class DownloadTarget(object):
    def __init__(self, langname, hash, url, filename=None):
        self.lang = langname
        self.dirname = os.path.join(pkgbuild_dir, langname)
        self.url = url.split("?")[0]  # Remove tracker/source nonsense
        if filename is None:
            self.fname = os.path.join(self.dirname, self.url.split("/")[-1])
        else:
            self.fname = os.path.join(self.dirname, filename)
        self.hash = hash

    def download_file(self):
        req = urllib.request.Request(self.url)
        for (k, v) in default_header.items():
            req.add_header(k, v)
        response = urllib.request.urlopen(req, context=default_ssl_ctx)
        data = response.read()
        with open(self.fname, "wb") as f:
            f.write(data)

    def download_hash(self):
        return sha256sum(self.fname)

    def validate_file(self):
        return self.hash == self.download_hash()

    def get_with_info(self):
        self.download_file()
        if not self.validate_file():
            print("Validation error for file " + self.fname)
            print("\t Expected hash: " + self.hash)
            print("\t   Actual hash: " + self.download_hash())
        else:
            print("Successfully downloaded + validated file " + self.fname)


targets = [
    DownloadTarget(
        "icu52",
        "e00c9c13875239aae4b0c8f9fa6fc8df8285568d318c13c5fe67fef883e9cabd",
        "https://download.swift.org/swift-4.2.4-release/ubuntu1604/swift-4.2.4-RELEASE/swift-4.2.4-RELEASE-ubuntu16.04.tar.gz",
    ),
]

if __name__ == "__main__":
    for target in targets:
        target.get_with_info()
