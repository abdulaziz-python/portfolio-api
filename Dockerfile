FROM python:3.11-slim

WORKDIR /app

# O'zgaruvchan argumentlar
ARG ENVIRONMENT=production
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV ENVIRONMENT=${ENVIRONMENT}
ENV DJANGO_SETTINGS_MODULE=portfolio.settings

# System paketlarini o'rnatish
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    libpq-dev \
    netcat-traditional \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Python paketlarini o'rnatish
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt gunicorn psycopg2-binary

# Ilovani ko'chirib olish
COPY . .

# Xavfsizlik
RUN useradd -ms /bin/bash django
RUN chown -R django:django /app
USER django

# Statik fayllarni to'plash
RUN python manage.py collectstatic --noinput

# Healthcheck
HEALTHCHECK --interval=30s --timeout=30s --start-period=5s --retries=3 \
    CMD curl -f http://localhost:8000/admin/login/ || exit 1

# Container ishga tushganda bajariladigan buyruq
CMD gunicorn portfolio.wsgi:application --bind 0.0.0.0:$PORT 