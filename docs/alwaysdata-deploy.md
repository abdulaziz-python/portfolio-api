# AlwaysData Deployment Guide

Bu hujjat Django loyihani AlwaysData serverlariga deploy qilish bo'yicha yo'riqnoma.

## Deploy qilish uchun tayyorgarlik

1. [AlwaysData](https://www.alwaysdata.com/) saytida hisob yarating
2. AlwaysData panelidan yangi sayt (site) yarating

## AlwaysData'da Web Application yaratish

1. AlwaysData admin paneliga kiring
2. Sites > Add a site bo'limiga o'ting
3. Quyidagi ma'lumotlarni kiriting:
   - Ism: `portfolio-api` (o'z loyihangiz nomini kiriting)
   - Domain: `api.abdulaziz.org.uz` yoki `username.alwaysdata.net` (standart domaindan foydalanish)
   - Tur: `Python WSGI`
   - Konfiguratsiya:
     - Path to WSGI file: `/path/to/project/wsgi.py`
     - Python versiyasi: `3.11` (loyihangizga mos versiya)
     - Working directory: `/path/to/project`
     - Environment variables: (quyida ko'rsatilgan)

## Ma'lumotlar bazasi sozlamalari

1. AlwaysData paneliga kiring
2. Databases > Add a database
3. PostgreSQL yoki MySQL ma'lumotlar bazasini tanlang
4. Kerakli ma'lumotlarni to'ldiring:
   - Nom
   - Foydalanuvchi nomi
   - Parol

## Environment o'zgaruvchilar

Environment > Variables bo'limida quyidagi o'zgaruvchilarni kiriting:

```
DATABASE_URL=postgresql://username:password@postgresql-username.alwaysdata.net:5432/username_dbname
SECRET_KEY=your-secret-key
DEBUG=false
ALLOWED_HOSTS=username.alwaysdata.net,api.abdulaziz.org.uz
TELEGRAPH_TOKEN=your-telegraph-token
```

## SSH orqali loyihani yuklash

1. SSH bilan AlwaysData serveriga ulaning:
   ```bash
   ssh username@ssh-username.alwaysdata.net
   ```

2. Kerakli direktoriyaga kiring (web sayt uchun ajratilgan joy):
   ```bash
   cd /home/username/www
   ```

3. Git repositoriyasini klonlang:
   ```bash
   git clone https://github.com/username/repository-name.git .
   ```

4. Kerakli paketlarni o'rnating:
   ```bash
   pip install -r requirements.txt
   ```

5. Statik fayllarni to'plang:
   ```bash
   python manage.py collectstatic --noinput
   ```

6. Migrationlarni bajaring:
   ```bash
   python manage.py migrate
   ```

## WSGI konfiguratsiyasi

AlwaysData uchun WSGI konfiguratsiyasi oddiy, standart wsgi.py fayli ishlaydi:

```python
import os
from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'portfolio.settings')

application = get_wsgi_application()
```

## Static fayllar konfiguratsiyasi

AlwaysData'da static fayllarni serverlash uchun `sites` bo'limida yangi `static` sayt yarating:

1. Sites > Add a site
2. Quyidagi ma'lumotlarni kiriting:
   - Nom: `portfolio-static`
   - Subdivision: `static.api.abdulaziz.org.uz` yoki subdirectory `/static`
   - Tur: `Static files`
   - Konfiguratsiya: 
     - Root directory: `/home/username/www/staticfiles`

## Domain sozlamalari

O'z domainigizni ulash uchun:

1. Domains > Add a domain
2. Custom domain qo'shing
3. DNS sozlamalarini AlwaysData'ga yo'naltiring
4. AlwaysData'da Sites bo'limida domainni bog'lang

## Yangilanishlar uchun

Loyihangizni yangilash uchun:

```bash
ssh username@ssh-username.alwaysdata.net
cd /home/username/www
git pull
python manage.py collectstatic --noinput
python manage.py migrate
```

## Xatoliklarni bartaraf etish

- Log fayllarni ko'rish: Logs bo'limiga kiring
- Xatolik bo'lsa, DEBUG=true qilib tekshiring
- Ma'lumotlar bazasi bog'lanish xatolari: DATABASE_URL parametrini tekshiring
- WSGI xatolari: web server logs orqali tekshiring

## Ba'zi maxsus sozlamalar

### HTTPS sozlash
AlwaysData automatik ravishda SSL sertifikatlarini boshqaradi, parametrlar bo'limida HTTPS ni yoqishingiz kerak.

### Statik fayllarni CloudFlare orqali boshqarish
Tez ishlatish uchun CloudFlare CDN bilan ishlatishingiz mumkin. Buning uchun domainlarni CloudFlare'ga yo'naltiring. 