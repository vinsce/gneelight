FROM ubuntu:latest

RUN apt-get update && \
    DEBIAN_FRONTEND=noninteractive apt-get install -yq flatpak flatpak-builder git

RUN flatpak remote-add --if-not-exists --from flathub https://flathub.org/repo/flathub.flatpakrepo \
    && flatpak install -y flathub org.gnome.Platform//40 \
    && flatpak install -y flathub org.gnome.Sdk//40

RUN cd /opt \
    && git clone https://github.com/vinsce/gneelight.git \
    && cd gneelight \
    && git checkout feature/github-actions \
    && git submodule update --init

WORKDIR /opt/gneelight/

# docker build -t gneelight-build-ubuntu -f Dockerfile .
# docker container run --privileged --rm -it --name gneelight-build gneelight-build-ubuntu /bin/bash
# ./flatbuild.sh