import urllib.request
import os.path
import hashlib

# Download location. Preferably either relative to script location or in some
# temporary location
download_folder = "downloads"

# Spoof a curl client so that some websites don't immediately 403 us
default_header = {"user-agent": "curl/7.82.0", "accept": "*/*"}

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
    def __init__(self, hash, url, filename=None):
        self.url = url.split("?")[0]  # Remove tracker/source nonsense
        if filename is None:
            self.fname = os.path.join(download_folder, self.url.split("/")[-1])
        else:
            self.fname = os.path.join(download_folder, filename)
        self.hash = hash

    def download_file(self):
        req = urllib.request.Request(self.url)
        for (k, v) in default_header.items():
            req.add_header(k, v)
        response = urllib.request.urlopen(req)
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
            print(f"Validation error for file {self.fname}")
            print(f"\t Expected hash: {self.hash}")
            print(f"\t   Actual hash: {self.download_hash()}")
        else:
            print(f"Successfully downloaded + validated file {self.fname}")


targets = [
    DownloadTarget(
        "e00c9c13875239aae4b0c8f9fa6fc8df8285568d318c13c5fe67fef883e9cabd",
        "https://download.swift.org/swift-4.2.4-release/ubuntu1604/swift-4.2.4-RELEASE/swift-4.2.4-RELEASE-ubuntu16.04.tar.gz",
    ),
    DownloadTarget(
        "48621912c242753ba37cad5145df375eeba41c81079df46f93ffb4896542e8fd",
        "https://static.rust-lang.org/dist/rust-1.16.0-x86_64-unknown-linux-gnu.tar.gz",
    ),
    DownloadTarget(
        "4fc8a9992de3e90191de369270ea4b6c1b171b7941743614cc50822ddc1fe654",
        "https://cache.ruby-lang.org/pub/ruby/2.4/ruby-2.4.1.tar.xz",
    ),
    DownloadTarget(
        "96fea14fd482bdee0ab128f962f7c38cad6528e14acd483da41e5603ed40a8a7",
        "https://download.racket-lang.org/installers/6.8/racket-6.8-x86_64-linux.sh",
    ),
    DownloadTarget(
        "a9a37c0860380ecd7b23aa06d61c20fc5bc6d95198029f3684c44a9d7e2952f2",
        "http://www.cpan.org/src/5.0/perl-5.24.0.tar.xz",
    ),
    DownloadTarget(
        "5113c06884f7de453ce57702abaac1d618307f33f6789fa870e87a59d772aca2",
        "https://www.lua.org/ftp/lua-5.3.3.tar.gz",
    ),
    DownloadTarget(
        "e5d8a6f629020c580473d8afcfcb06c3966d01929f7b734f41dc0c737cd8ea3f",
        "https://github.com/ocaml/ocaml/archive/4.05.0.tar.gz",
        "ocaml-4.05.0.tar.gz",
    ),
    DownloadTarget(
        "71514386adf3e963df087c2044a0b3747900b8b1fc8da3a99f0a0ae9180d300b",
        "https://www.php.net/distributions/php-7.1.4.tar.xz",
    ),
    DownloadTarget(
        "d8910cf0dd90be84c07df179512cf2e36659a92726e67e8dc8bc8b457fe6e5ee",
        "https://nodejs.org/download/release/v7.9.0/node-v7.9.0-linux-x64.tar.xz",
    ),
    DownloadTarget(
        "95ac7d2316fb7698039267265716dd2159fa5b49f0e0dc6e469c80ad59072926",
        "https://repo1.maven.org/maven2/org/jruby/jruby-dist/9.1.7.0/jruby-dist-9.1.7.0-bin.tar.gz",
    ),
    DownloadTarget(
        "5ee68290db00ca0b79d57bc3a5bdce470de9ce9da0b098a7ce6c504605856c8f",
        "https://downloads.haskell.org/~ghc/8.0.2/ghc-8.0.2-x86_64-deb8-linux.tar.xz",
    ),
    DownloadTarget(
        "3da8070567601b89a9b8235eddaae13c66415abbedc8aea2d405670228b03d8f",
        "https://storage.googleapis.com/dart-archive/channels/dev/release/1.24.0-dev.0.0/sdk/dartsdk-linux-x64-release.zip",
    ),
    DownloadTarget(
        "c7549124d90504027212a99176635b215ab11c12eadc995e89e7d019529d796f",
        "https://github.com/chapel-lang/chapel/releases/download/1.15.0/chapel-1.15.0.tar.gz",
    ),
    DownloadTarget(
        "835bfcb0cf56457a7c5f953f5fd7d6a37b7a68eb23dc0fb3d9161def833345ea",
        "https://download.microsoft.com/download/A/F/6/AF610E6A-1D2D-47D8-80B8-F178951A0C72/Binaries/dotnet-dev-ubuntu.16.10-x64.1.0.0-preview2-1-003177.tar.gz",
    ),
    DownloadTarget(
        "b5b27fdbc31b1d05b6a898f3c192d8a5083050562b29c19eb9eb018ba4482bd8",
        "https://downloads.sourceforge.net/project/freepascal/Linux/3.0.2/fpc-3.0.2.x86_64-linux.tar?ts=gAAAAABiNqyqJ-rKWKDERLIN7kEGe_fEFqRllTIll0r4AbTB9kAFSZDfIeCI-0mZO_Jj_FSmpnRcd_W_EV8m43QmILXjtzCFzg%3D%3D&r=https%3A%2F%2Fsourceforge.net%2Fprojects%2Ffreepascal%2Ffiles%2FLinux%2F3.0.2%2Ffpc-3.0.2.x86_64-linux.tar%2Fdownload",
    ),
    # The HHVM commit corresponding to tag HHVM-3.19.2
    DownloadTarget(
        "063471fd864c4a3b70f47754ef667e32bcab589c5f4ad12e2c561f0d9744a565",
        "https://github.com/facebook/hhvm/archive/8e7759b4b00535d65969dec6a56a03b4ed238b35.zip",
        "hhvm-3.19.2.zip",
    ),
]

if __name__ == "__main__":
    for target in targets:
        target.get_with_info()
