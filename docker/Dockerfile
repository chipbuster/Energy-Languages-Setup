FROM ubuntu:16.10

RUN useradd -ms /bin/bash user
USER user
WORKDIR /home/user

COPY preinstall_setup/ preinstall_setup/
COPY pkgbuilds/ pkgbuilds/
COPY prerequisites/ prerequisites/
COPY install_deps.sh install_deps.sh
COPY install_langs.sh install_langs.sh

WORKDIR /home/user/preinstall_setup/
USER root
RUN bash initial_install.sh
USER user

RUN python3 download_files.py
WORKDIR /home/user
RUN bash install_deps.sh
RUN bash install_langs.sh

ENTRYPOINT ["bash", "-l"]