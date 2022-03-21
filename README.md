# Energy Languages Benchmark Setup

This repository setup code for the [Energy Languages](https://github.com/greensoftwarelab/Energy-Languages)
with the goal of providing as similar an environment as possible to the 2017
paper published by the Green Software Lab.[^1]

### Rationale and Background

The Energy Languages benchmark is becoming more commonly cited, for example, in
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
requires bare-metal installation, as [Docker and virtualization are known to
cause increases in energy usage](https://www.sciencedirect.com/science/article/abs/pii/S0164121218301456)
Another reason, however, might simply be that installing the software needed for
the benchmark is highly nontrivial. The paper tested approximately 30 language
implementations, most of which are not available in the OS repositories, and many
which are installed at nonstandard paths. In addition (to the best of my knowledge)
there is not an installation script or image provided by the authors.

Adding to the difficulties, many of the original implementations which were used
in the paper are either no longer available or are very difficult to find, and
even when they can be found, installation on older systems can be challenging
due to [expiration of SSL certificates in the certificate store](https://askubuntu.com/questions/1366704/how-to-install-latest-ca-certificates-on-ubuntu-14).

This repository is an attempt to rectify this problem. Ideally, once the repository
is complete, it will have the framework code in order to allow the following:

- Installation of language compilers/runtimes on a native (bare-metal) install
  of Ubuntu 16.10, downloading the runtimes over the internet from their
  upstream sites.
- Installation of language compilers/runtimes on a native (bare-metal) install
  of Ubuntu 16.10, downloading the runtimes from a single source to avoid
  issues with SSL expiry.
- A Dockerfile to build a Docker image for the benchmarks.
- (Possible extension) Installation of language compilers/runtimes with more
  modern versions, onto an Ubuntu 22.04-based system.

As of time of writing, I have not decided what the correct approach is for
doing this (considering using Makedeb, but I need to see if it works on
older versions of Ubuntu first.)

## Language Versions

This is a table of languages used in the paper and the version used. I am targeting
the original 2017 paper---no new languages (e.g. Julia) or updated versions.
The first two columns come from [the project website's setup page](https://sites.google.com/view/energy-efficiency-languages/setup?authuser=0)
The last column of the table tells you how the language is installed in these scripts:

- "Repository" indicates that the version in the system repositories matched what
  was used in the paper.
- "Binary" indicates a binary installation from the upstream source site. This
  is the preferred method where it is available.
- "Source" indicates that the binary builds were not available. Instead, the
  source code for the appropriate version is downloaded and compiled with
  as-close-to-default compilation flags as possible.
- Any other entry indicates that the exact version of the software was unavailable:
  see the "Known Mismatches" sections for details.

| Language   | Paper Version          | Repo Version     |
| ---------- | ---------------------- | ---------------- |
| Ada        | GNAT 6.2.0             | Repository       |
| C          | gcc 6.2.0              | Repository       |
| C#         | dotnet 1.0.1           | Binary           |
| C++        | g++ 6.2.0              | Repository       |
| Chapel     | chpl 1.15.0            | Source           |
| Dart       | Dart VM 1.24.0-dev.0.0 | Binary           |
| Erlang     | Erlang 7.3.1.2         | Repository       |
| F#         | dotnet 1.0.1           | Binary           |
| Fortran    | ifort 17.0.3           | Latest OneAPI    |
| Go         | go go1.6.3             | Repository       |
| Hack       | HipHop VM 3.19.2       | Source           |
| Haskell    | ghc 8.0.2              | Binary           |
| Java       | jdk 1.8.0_121          | License issues   |
| JavaScript | node 7.9.0             | Binary           |
| Jruby      | jruby 9.1.7.0          | Binary           |
| Lisp       | SBCL 1.3.3debian       | Repository       |
| Lua        | Lua 5.3.3              | Source           |
| OCaml      | ocamlopt 4.05.0        | Source           |
| Pascal     | fpc 3.0.2              | Binary           |
| Perl       | perl 5.24.0            | Source           |
| PHP        | php 7.1.4              | Source           |
| Python     | python 3.5.2           | Repository       |
| Racket     | raco 6.8               | Binary           |
| Ruby       | ruby 2.4.1             | Source           |
| Rust       | rustc 1.16.0           | Binary           |
| Swift      | swift 4.0-dev          | 4.2.4-Release    |
| TypeScript | node 7.9.0             | Typescript 2.3.1 |

#### Known Mismatches

Licensing restrictions prevent me from distributing the appropriate Java runtime,
or from acquiring the version of ifort used in the paper. The user will need to
acquire and install Java themselves. `ifort` has been replaced with the version
offered by the Intel OneAPI HPC pack.

The version of Swift that was used for this paper appears to have been a nightly
alpha build. Unfortunately, those binaries are no longer available on
downloads.swift.com, and the build appears to rely on branch names from dependencies
that no longer exist (e.g attempting to check out "master" from the LLVM project
now fails).

Since I have no desire to go through 10 different repositories and attempt to infer
what commit a nonexistent branch might have been pointing to on a specific day
in 2017, I have instead substituted the 4.2 release Swift, which is the earliest
binary build for Swift which is still generally available.

Finally, the authors list "node 7.9.0" as the version of TypeScript used, which
doesn't actually tell us anything about what version of `tsc` was used. Looking
at release history, the first version of Typescript to be released after Node 7.9.0
was Typescript 2.3.1, so I am using that as a guess for the TS compiler version.

[^1]: "Energy Efficiency across Programming Languages: How does Energy, Time and Memory Relate?", Rui Pereira, Marco Couto, Francisco Ribeiro, Rui Rua, Jácome Cunha, João Paulo Fernandes, and João Saraiva. In Proceedings of the 10th International Conference on Software Language Engineering (SLE '17)