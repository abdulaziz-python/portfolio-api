#!/bin/bash
# Build statik fayllarni to'plash skripti

echo "Building static files..."
python3 -m pip install -r requirements.txt

# Staticfiles direktoryasini tayyorlash
mkdir -p staticfiles_build/static

# Static va media fayllarni to'plash
python3 manage.py collectstatic --noinput

# Vercel uchun statik fayllarni to'g'ri joylashtirish
cp -r static/ staticfiles_build/
cp -r staticfiles/ staticfiles_build/static/

echo "Build completed." 