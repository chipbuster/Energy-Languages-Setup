#!/usr/bin/env python3

import ssl
import urllib.request
import os
import hashlib
import tempfile

import subprocess

# Get the path to the pkgbuilds directory
filepath = os.path.abspath(__file__)
pkgbuild_dir = os.path.dirname(filepath)

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


class HTTPTarget(object):
    def __init__(self, langname, hash, url, filename=None):
        self.lang = langname
        self.dirname = os.path.join(pkgbuild_dir, langname)
        self.url = url.split("?")[0]  # Remove tracker/source nonsense
        if filename is None:
            self.fname = os.path.join(self.dirname, self.url.split("/")[-1])
        else:
            self.fname = os.path.join(self.dirname, filename)
        self.hash = hash

    def download_file(self, override=False):
        req = urllib.request.Request(self.url)
        if os.path.isfile(self.fname) and not override:
            return
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


class GitTarget(object):
    def __init__(self, langname, repo_url, commit_hash=None, filename=None):
        self.lang = langname
        self.dirname = os.path.join(pkgbuild_dir, langname)
        self.git_stem = ".".join(repo_url.split(".")[0:-1]).split("/")[-1]
        self.repo_path = os.path.join(tempfile.gettempdir(), self.git_stem)
        self.url = repo_url
        if filename is None:
            self.fname = os.path.join(self.dirname, self.git_stem) + ".tar.xz"
        else:
            self.fname = os.path.join(self.dirname, filename)
        self.commit = commit_hash

    def checkout_repo(self):
        if os.path.exists(self.repo_path):
            print("[ERR]: There is already an item at " + self.repo_path)
            print("This will cause git clone to fail. Delete it and run again.")
        subprocess.run(["git", "clone", self.url, self.repo_path]).check_returncode()
        cur_dir = os.getcwd()
        os.chdir(self.repo_path)
        if self.commit is not None:
            subprocess.run(["git", "checkout", self.commit]).check_returncode()
        subprocess.run(
            ["git", "submodule", "update", "--init", "--recursive"]
        ).check_returncode()

        os.chdir(cur_dir)

    def get_with_info(self):
        if os.path.isfile(self.fname):
            return
        print("Checking out repo " + self.url + " to " + self.repo_path)
        if self.commit is not None:
            print("\tCommit hash: " + self.commit)
        # self.checkout_repo()

        print("Compressing archive")
        os.environ["XZ_OPT"] = "-T0"
        subprocess.run(
            [
                "tar",
                "-C",
                os.path.dirname(self.repo_path),
                "-cJvf",
                self.fname,
                os.path.basename(self.repo_path),
            ]
        ).check_returncode()

        cksum = sha256sum(self.fname)
        print("Repo tarball at " + self.fname + " with SHA256 hash " + cksum)


targets = [
    HTTPTarget(
        "Swift",
        "e00c9c13875239aae4b0c8f9fa6fc8df8285568d318c13c5fe67fef883e9cabd",
        "https://download.swift.org/swift-4.2.4-release/ubuntu1604/swift-4.2.4-RELEASE/swift-4.2.4-RELEASE-ubuntu16.04.tar.gz",
    ),
    HTTPTarget(
        "Rust",
        "48621912c242753ba37cad5145df375eeba41c81079df46f93ffb4896542e8fd",
        "https://static.rust-lang.org/dist/rust-1.16.0-x86_64-unknown-linux-gnu.tar.gz",
    ),
    HTTPTarget(
        "Ruby",
        "4fc8a9992de3e90191de369270ea4b6c1b171b7941743614cc50822ddc1fe654",
        "https://cache.ruby-lang.org/pub/ruby/2.4/ruby-2.4.1.tar.xz",
    ),
    HTTPTarget(
        "Racket",
        "96fea14fd482bdee0ab128f962f7c38cad6528e14acd483da41e5603ed40a8a7",
        "https://download.racket-lang.org/installers/6.8/racket-6.8-x86_64-linux.sh",
    ),
    HTTPTarget(
        "Perl",
        "a9a37c0860380ecd7b23aa06d61c20fc5bc6d95198029f3684c44a9d7e2952f2",
        "http://www.cpan.org/src/5.0/perl-5.24.0.tar.xz",
    ),
    HTTPTarget(
        "Lua",
        "5113c06884f7de453ce57702abaac1d618307f33f6789fa870e87a59d772aca2",
        "https://www.lua.org/ftp/lua-5.3.3.tar.gz",
    ),
    HTTPTarget(
        "OCaml",
        "e5d8a6f629020c580473d8afcfcb06c3966d01929f7b734f41dc0c737cd8ea3f",
        "https://github.com/ocaml/ocaml/archive/4.05.0.tar.gz",
        "ocaml-4.05.0.tar.gz",
    ),
    HTTPTarget(
        "PHP",
        "71514386adf3e963df087c2044a0b3747900b8b1fc8da3a99f0a0ae9180d300b",
        "https://www.php.net/distributions/php-7.1.4.tar.xz",
    ),
    HTTPTarget(
        "JavaScript",
        "d8910cf0dd90be84c07df179512cf2e36659a92726e67e8dc8bc8b457fe6e5ee",
        "https://nodejs.org/download/release/v7.9.0/node-v7.9.0-linux-x64.tar.xz",
    ),
    HTTPTarget(
        "JRuby",
        "95ac7d2316fb7698039267265716dd2159fa5b49f0e0dc6e469c80ad59072926",
        "https://repo1.maven.org/maven2/org/jruby/jruby-dist/9.1.7.0/jruby-dist-9.1.7.0-bin.tar.gz",
    ),
    HTTPTarget(
        "Haskell",
        "5ee68290db00ca0b79d57bc3a5bdce470de9ce9da0b098a7ce6c504605856c8f",
        "https://downloads.haskell.org/~ghc/8.0.2/ghc-8.0.2-x86_64-deb8-linux.tar.xz",
    ),
    HTTPTarget(
        "Dart",
        "3da8070567601b89a9b8235eddaae13c66415abbedc8aea2d405670228b03d8f",
        "https://storage.googleapis.com/dart-archive/channels/dev/release/1.24.0-dev.0.0/sdk/dartsdk-linux-x64-release.zip",
    ),
    HTTPTarget(
        "Chapel",
        "c7549124d90504027212a99176635b215ab11c12eadc995e89e7d019529d796f",
        "https://github.com/chapel-lang/chapel/releases/download/1.15.0/chapel-1.15.0.tar.gz",
    ),
    HTTPTarget(
        "Dotnet",
        "828af612b3e691f27d93153c3c7fd561e041535e907e9823f206ccab51030ecf",
        "https://dotnetcli.blob.core.windows.net/dotnet/Sdk/1.0.1/dotnet-dev-ubuntu.16.10-x64.1.0.1.tar.gz",
    ),
    HTTPTarget(
        "Pascal",
        "b5b27fdbc31b1d05b6a898f3c192d8a5083050562b29c19eb9eb018ba4482bd8",
        "https://downloads.sourceforge.net/project/freepascal/Linux/3.0.2/fpc-3.0.2.x86_64-linux.tar?ts=gAAAAABiNqyqJ-rKWKDERLIN7kEGe_fEFqRllTIll0r4AbTB9kAFSZDfIeCI-0mZO_Jj_FSmpnRcd_W_EV8m43QmILXjtzCFzg%3D%3D&r=https%3A%2F%2Fsourceforge.net%2Fprojects%2Ffreepascal%2Ffiles%2FLinux%2F3.0.2%2Ffpc-3.0.2.x86_64-linux.tar%2Fdownload",
    ),
    HTTPTarget(
        "Dotnet",
        "860a22f2adc783a1ab10cb373109682d32435c76b9045bc9966d097512bec937",
        "https://download.microsoft.com/download/2/4/A/24A06858-E8AC-469B-8AE6-D0CEC9BA982A/dotnet-ubuntu-x64.1.0.5.tar.gz",
    ),
    HTTPTarget(
        "TypeScript",
        "f3232e83869048f340e6ec438d6e0e0169f1213524d1eba7da9385b3f00dcc86",
        "http://registry.npmjs.org/typescript/-/typescript-2.3.1.tgz",
    ),
    HTTPTarget(
        "Python",
        "a01810ddfcec216bcdb357a84bfaafdfaa0ca42bbdaa4cb7ff74f5a9961e4041",
        "https://www.python.org/ftp/python/3.6.1/Python-3.6.1.tar.xz",
    ),
    GitTarget(
        "Hack",
        "https://github.com/facebook/hhvm.git",
        commit_hash="8e7759b4b00535d65969dec6a56a03b4ed238b35",
    ),
]

if __name__ == "__main__":
    for target in targets:
        target.get_with_info()
