#!/usr/bin/env bash
flatpak-builder --repo=./../repo -v --force-clean --install-deps-from=flathub build-dir me.vinsce.Gneelight.json
flatpak build-bundle ./../repo gneelight.flatpak me.vinsce.Gneelight