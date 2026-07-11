#!/usr/bin/env bash
set -euo pipefail

cd /home/Spocker/mechanic-board

bash scripts/deploy.sh > /tmp/mechanic-board.log 2>&1 &

if command -v flatpak >/dev/null 2>&1; then
  flatpak run com.google.Chrome --new-window http://localhost:8000/admin/
else
  xdg-open http://localhost:8000/admin/ >/dev/null 2>&1 || true
fi
