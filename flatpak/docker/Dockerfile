# Docker container to simulate GitHub flatbuild workflow

FROM ubuntu:latest

RUN apt-get update && \
    DEBIAN_FRONTEND=noninteractive apt-get install -yq flatpak flatpak-builder git

RUN flatpak remote-add --if-not-exists --from flathub https://flathub.org/repo/flathub.flatpakrepo \
    && flatpak install -y flathub org.gnome.Platform//42 \
    && flatpak install -y flathub org.gnome.Sdk//42

RUN cd /opt \
    && git clone https://github.com/vinsce/gneelight.git \
    && cd gneelight \
    && git checkout master \
    && git submodule update --init

# COPY ./ /opt/gneelight/
# docker build -t gneelight-build-ubuntu -f flatpak/docker/Dockerfile .

WORKDIR /opt/gneelight/

# docker build -t gneelight-build-ubuntu -f Dockerfile .
# docker container run --privileged --rm -it --name gneelight-build gneelight-build-ubuntu /bin/bash
# ./flatbuild.sh
