# Energy Languages Benchmark Setup

This repository setup code for the [Energy Languages](https://github.com/greensoftwarelab/Energy-Languages)
with the goal of providing as similar an environment as possible to the 2017
paper published by the Green Software Lab.[^1]

# Quick Start

TODO

## Rationale and Background

The Energy Languages benchmark is becoming more commonly cited in discussions
about choosing programming languages, for example, in
[this article about crypto efficiency](https://cryptomode.com/c-is-the-most-energy-efficient-and-fastest-programming-language-study-finds/)
or [this AWS announcement about switching to Rust](https://aws.amazon.com/blogs/opensource/sustainability-with-rust/).

This paper has generated some controversy on the internet, with several notable
users pointing out strange discrepancies in the results. See e.g.
[this Twitter thread](https://mobile.twitter.com/_rsc/status/1496352325157457922),
which specifically calls out the gap between C and C++ in the benchmarks. There
have also been criticisms that TypeScript takes on average 7x more time than
JavaScript and all sorts of other discussions about how the results in this paper
are suspicious.

However, in spite of the Energy Languages repository being [relatively active](https://github.com/greensoftwarelab/Energy-Languages)
for a research project repository, I have not been able to find any records of
someone reproducing the results in the paper. This is in spite of the fact that
several users, including the current maintainer of the CLBG, Issac Gouy, have
speculated that [the TypeScript results may contain a typo](https://www.reddit.com/r/rust/comments/szpgau/russ_cox_on_sustainability_with_rust_post_by_aws/hy8bino).

Why have there been so few replications? One reason might be because energy usage
measurement requires bare-metal installation, as [Docker and virtualization are
known to cause increases in energy
usage](https://www.sciencedirect.com/science/article/abs/pii/S0164121218301456).
Another reason, however, might simply be that installing the software needed for
the benchmark is highly nontrivial. The paper tested approximately 30 language
implementations, most of which are not available in the OS repositories, and
many which are installed at nonstandard paths. In addition, (to the best of my
knowledge) there is not an installation script or image provided by the authors.

Adding to the difficulties, many of the original implementations which were used
in the paper are either no longer available or are very difficult to find, and
even when they can be found, installation on older systems can be challenging
due to [expiration of SSL certificates in the certificate store](https://askubuntu.com/questions/1366704/how-to-install-latest-ca-certificates-on-ubuntu-14).

This repository is an attempt to rectify this problem. It contains a set of
bash/python/makedeb scripts which install the language runtimes used in the paper
at the locations specified in the repository (or as close as I could get---see
"Language Versions" section for caveats).

## Language Versions

This is a table of languages used in the paper and the version used. I am targeting
the original 2017 paper---no new languages (e.g. Julia) or updated versions.
The first two columns come from [the project website's setup page](https://sites.google.com/view/energy-efficiency-languages/setup?authuser=0).
The last column of the table tells you how the language is installed in these scripts:

- "Repository" indicates that the version in the system repositories matched what
  was used in the paper.
- "Binary" indicates a binary installation of the appropriate version from the
  upstream source site. Due to reproducibility concerns when compiling from source,
  this is the preferred method when available.
- "Source" indicates that the binary builds were not available. Instead, the
  source code for the appropriate version is downloaded and compiled with
  as-close-to-default compilation flags as possible.
- Any other entry indicates that the exact version of the software was unavailable:
  see the "Known Mismatches" sections for details.

| Language   | Paper Version          | Repo Version         |
| ---------- | ---------------------- | -------------------- |
| Ada        | GNAT 6.2.0             | Repository           |
| C          | gcc 6.2.0              | Repository           |
| C#         | dotnet 1.0.1           | Binary               |
| C++        | g++ 6.2.0              | Repository           |
| Chapel     | chpl 1.15.0            | Source               |
| Dart       | Dart VM 1.24.0-dev.0.0 | Binary               |
| Erlang     | Erlang 7.3.1.2         | Repository           |
| F#         | dotnet 1.0.1           | Binary               |
| Fortran    | ifort 17.0.3           | **Latest OneAPI**    |
| Go         | go go1.6.3             | Repository           |
| Hack       | HipHop VM 3.19.2       | Source               |
| Haskell    | ghc 8.0.2              | Binary               |
| Java       | jdk 1.8.0_121          | **License issues**   |
| JavaScript | node 7.9.0             | Binary               |
| Jruby      | jruby 9.1.7.0          | Binary               |
| Lisp       | SBCL 1.3.3debian       | Repository           |
| Lua        | Lua 5.3.3              | Source               |
| OCaml      | ocamlopt 4.05.0        | Source               |
| Pascal     | fpc 3.0.2              | Binary               |
| Perl       | perl 5.24.0            | Source               |
| PHP        | php 7.1.4              | Source               |
| Python     | python 3.5.2           | Repository           |
| Racket     | raco 6.8               | Binary               |
| Ruby       | ruby 2.4.1             | Source               |
| Rust       | rustc 1.16.0           | Binary               |
| Swift      | swift 4.0-dev          | **4.2.4-Release**    |
| TypeScript | node 7.9.0             | **Typescript 2.3.1** |

### Known Mismatches

##### Java

License agreements restrict me from distributing the appropriate Java runtime.
In order to obtain it, go to https://www.oracle.com/java/technologies/javase/javase8-archive-downloads.html
and search for "8u121". Then download the file named "jdk-8u121-linux-x64.tar.gz".

Place this file in the `Java` directory of the installers and run `makedeb -si`
to install the Java runtimes.

##### Fortran

Comments on the Intel Community Forums suggest that, without an Intel Parallel
Studio XE paid support plan, Intel will not provide binaries for ifort 17.0.6
anymore. Presumably, this policy also applies to the older 17.0.3 used by the
paper. `ifort` has been replaced with the version offered by the Intel OneAPI
HPC pack.

Installation of the OneAPI HPC pack is scripted, but will still require
interaction from the user. It also requires an active internet connection, since
the OneAPI installers actively download material over the internet.

##### Swift

The version of Swift that was used for this paper appears to have been a nightly
alpha build. Unfortunately, those binaries are no longer available on
downloads.swift.com, and the build appears to rely on branch names from dependencies
that no longer exist (e.g attempting to check out "master" from the LLVM project
now fails).

Since I have no desire to go through 10 different repositories and attempt to infer
what commit a nonexistent branch might have been pointing to on a specific day
in 2017, I have instead substituted the 4.2 release Swift, which is the earliest
binary build for Swift which is still generally available.

##### TypeScript

The authors list "node 7.9.0" as the version of TypeScript used, which
doesn't actually tell us anything about what version of `tsc` was used. Looking
at release history, the first version of Typescript to be released after Node 7.9.0
was Typescript 2.3.1, so I am using that as a guess for the TS compiler version.

## Notes about certificate expiry

Due to SSL certificate expiry, the version of Firefox that comes with Ubuntu 16.10
can no longer access all of GitHub: specifically, the ability to view files or
download ZIPs/git repositories no longer works.

In order to grab this repository, you can use the following command to grab
this repository:

```
wget --no-check-certificate 'https://github.com/chipbuster/Energy-Languages-Setup/archive/refs/heads/trunk.zip'
```

If you need to access the internet with a web browser, you can also manually add
an exception for firefox.com to access the latest version of firefox. These
Firefox downloads come with their own (modern) certificate stores, so they will
be able to access most websites.

In general, `wget` and `curl` may not be able to successfully verify certificates
on 16.10. All scripts and programs in this repository avoid this issue by
disabling SSL verification and relying on SHA256 hashes of the downloaded files
to ensure that nothing has been tampered with.

[^1]: "Energy Efficiency across Programming Languages: How does Energy, Time and Memory Relate?", Rui Pereira, Marco Couto, Francisco Ribeiro, Rui Rua, Jácome Cunha, João Paulo Fernandes, and João Saraiva. In Proceedings of the 10th International Conference on Software Language Engineering (SLE '17)
