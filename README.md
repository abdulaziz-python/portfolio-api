# Portfolio Backend

Bu proyekt Django, Django REST Framework, Celery va Django Unfold orqali qurilgan portfolio backend tizimidir.

## Xususiyatlari

- **Admin Panel** - Django Unfold yordamida chiroyli admin panel
- **Blog** - Blog postlar (markdown formati qo'llanilgan)
- **Proyektlar** - Ko'rsatilgan proyektlar
- **Ko'nikmalar** - Qobiliyatlar ro'yxati
- **API** - REST API barcha ma'lumotlarga kirish uchun
- **Background Tasks** - Celery tasklari orqali avtomatlashtirish

## O'rnatish

1. Repositoryni klonlash:
```bash
git clone <repository-url>
cd portfolio
```

2. Virtual muhit yaratish va faollashtirish:
```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate  # Windows
```

3. Kerakli paketlarni o'rnatish:
```bash
pip install -r requirements.txt
```

4. Ma'lumotlar bazasini tayyorlash:
```bash
python manage.py migrate
```

5. Admin foydalanuvchi yaratish:
```bash
python manage.py createsuperuser
```

6. Statik fayllarni to'plash:
```bash
python manage.py collectstatic
```

## Ishga tushirish

1. Django serverni ishga tushirish:
```bash
python manage.py runserver
```

2. Redis serverini ishga tushirish (Celery uchun):
```bash
redis-server
```

3. Celery worker ishga tushirish:
```bash
celery -A portfolio worker -l info
```

4. Celery beat ishga tushirish:
```bash
celery -A portfolio beat -l info
```

## API Endpointlari

- Blog postlar: `/api/posts/`
- Alohida blog post: `/api/posts/<slug>/`
- Proyektlar: `/api/projects/`
- Alohida proyekt: `/api/projects/<slug>/`
- Ko'nikmalar: `/api/skills/`

## Admin Panel

Admin panelga `/admin/` orqali kirishingiz mumkin. U yerda:

- Blog postlarini boshqarish
- Proyektlarni boshqarish
- Ko'nikmalarni boshqarish

## Celery Tasks

- `blog.tasks.cleanup_old_posts`: Eski blog postlarini o'chirish (default: 1 yildan eski)
- `projects.tasks.cleanup_unused_images`: Ishlatilmayotgan rasm fayllarini o'chirib tashlash 

## Telegraph API Integratsiya

Bu loyiha [Telegraph API](https://telegra.ph/api) bilan chuqur integratsiya qilingan. Barcha ma'lumotlar Telegraph-da saqlanadi va boshqariladi.

### Asosiy xususiyatlar:

- **Rasmlar Telegraphda saqlanadi**, mahalliy serverga yuklash o'rniga
- **Blog postlari va loyihalar telegraphda** jsonlashtiriladi va avtomatik ravishda sinxronlashtiriladi
- **Skill ikonkalari ham Telegraphda** saqlanadi
- **Ma'lumotlar o'qish/yozish** faqat Telegraph API orqali amalga oshiriladi
- **Real-time sinxronizatsiya** - o'zgarishlar Telegraph-da va backend bazada sinxronlashtirilgan

### Telegraph API endpointlari:

- `POST /api/telegraph/token/` - Yangi Telegraph token olish (admin huquqi bilan)
- `POST /api/telegraph/upload-image/` - Rasmni Telegraphga yuklash
- `GET /api/telegraph/page-info/?path=XXX` - Telegraph sahifasi haqida ma'lumot olish

### Qo'shimcha API endpointlari:

- `POST /api/posts/{slug}/sync_from_telegraph/` - Blog postni Telegraphdan sinxronlash
- `POST /api/projects/{slug}/sync_from_telegraph/` - Loyihani Telegraphdan sinxronlash

### Telegraph token olish uchun:

1. [Telegraph](https://telegra.ph/) sahifasiga tashrif buyuring
2. "..." menyusini bosib, hisob yarating
3. "Your account" bo'limiga o'ting va `access_token` qiymatini nusxalash
4. Yoki Telegraph API orqali token olish: `https://api.telegra.ph/createAccount?short_name=YourName&author_name=YourName`
5. Yoki backendning `/api/telegraph/token/` endpointini ishlatish
6. Tokenni `.env` fayliga qo'shing:

```
TELEGRAPH_TOKEN=your-token-here
```

## Yaxshilangan API xususiyatlari

- Blog va loyihalar uchun ko'rishlar hisobi
- Blogga sharhlar qo'shish imkoniyati
- Loyihalarni tanlangan qilish va saralash
- Ma'lumotlarni samarali qilish uchun optimallashtirilgan so'rovlar
- Telegraph bilan avtomatik sinxronizatsiya 