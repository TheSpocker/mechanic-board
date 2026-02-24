#!/usr/bin/env bash

cd /home/Spocker/mechanic-board

podman compose up -d

flatpak run com.google.Chrome --new-window http://localhost:8000/
