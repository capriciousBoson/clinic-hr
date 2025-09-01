#!/usr/bin/env bash
set -e

# 1) Install Python deps & collect Django static (admin, etc.)
python -m pip install -r requirements.txt
python manage.py collectstatic --noinput

# 2) Build the Vue app
cd ../_frontend/app
npm ci
npm run build
cd -  # back to _backend

# 3) Prepare Vercel static output
#    - Put the Vue dist at the web root
#    - Also expose Django 'staticfiles' under /static for admin assets
mkdir -p .vercel/output/static
cp -r ../_frontend/app/dist/* .vercel/output/static/

# If you want Django admin static too (recommended):
mkdir -p .vercel/output/static/static/
cp -r staticfiles/. .vercel/output/static/static/
chmod +x _backend/build_files.sh
