#!/usr/bin/env bash
set -euo pipefail

cd "$(dirname "$0")/.."
cd app

export DJANGO_SETTINGS_MODULE=config.settings
export PYTHONUNBUFFERED=1

python manage.py migrate --noinput
python manage.py collectstatic --noinput
exec python manage.py runserver 0.0.0.0:${PORT:-8000}
