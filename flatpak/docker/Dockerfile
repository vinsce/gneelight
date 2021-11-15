FROM ubuntu:latest

RUN apt-get update && \
    DEBIAN_FRONTEND=noninteractive apt-get install -yq flatpak flatpak-builder git

RUN cd /opt \
    && git clone https://github.com/vinsce/gneelight.git \
    && cd gneelight \
    && git checkout feature/github-actions \
    && git submodule update --init

RUN flatpak remote-add --if-not-exists --from flathub https://flathub.org/repo/flathub.flatpakrepo \
    && flatpak install -y flathub org.gnome.Platform//40 \
    && flatpak install -y flathub org.gnome.Sdk//40 \

RUN cd /opt/gneelight/flatpak && \
    ./flatbuild.sh