#!/usr/bin/env bash
# Render build script. Render build command: bash build.sh
set -o errexit

pip install -r requirements.txt
python manage.py collectstatic --no-input
python manage.py migrate --no-input
python manage.py seed_demo

# Optional: create an admin on first deploy when these env vars are set on Render.
if [[ -n "${DJANGO_SUPERUSER_USERNAME:-}" ]]; then
  python manage.py createsuperuser --no-input || true  # ignore "already exists"
fi
