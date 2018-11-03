#!/usr/bin/env bash
flatpak-builder --repo=./../repo --force-clean build-dir me.vinsce.Gneelight.json
flatpak build-bundle ./../repo gneelight.flatpak me.vinsce.Gneelight