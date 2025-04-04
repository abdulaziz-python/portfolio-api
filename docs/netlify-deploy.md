# Netlify Deployment Guide

Bu hujjat Django loyihani Netlify serverlariga deploy qilish bo'yicha yo'riqnoma.

## Deploy qilish uchun tayyorgarlik

1. Netlify hisob qaydnomasi yarating: [Netlify](https://www.netlify.com/) saytida.
2. GitHub repositoriyangizni Netlify bilan bog'lang.

## Deploy sozlamalari

Netlify'da quyidagi sozlamalarni o'rnating:

| Sozlama | Qiymat |
|---------|--------|
| Build command | `./build_files.sh` |
| Publish directory | `staticfiles_build` |
| Functions directory | `netlify/functions` |

## Environment o'zgaruvchilar

Netlify'da quyidagi environment o'zgaruvchilarni o'rnating:

```
DATABASE_URL=postgresql://username:password@hostname:port/dbname
SECRET_KEY=your-secret-key
DEBUG=false
ALLOWED_HOSTS=*.netlify.app,*.abdulaziz.org.uz
TELEGRAPH_TOKEN=your-telegraph-token
```

## Netlify Functions bilan ishlash

Loyiha Netlify Functions'ni qo'llab-quvvatlaydi va quyidagi fayllar orqali sozlangan:

- `netlify/functions/api.js`: API so'rovlar uchun
- `netlify/functions/admin.js`: Admin paneliga kirish uchun
- `wsgi.py`: Netlify Functions bilan Django o'rtasidagi bog'lovchi

## Deploy jarayoni

1. O'zgarishlarni GitHub'ga push qiling:

```bash
git add .
git commit -m "Netlify deploy uchun tayyorgarlik"
git push origin master
```

2. Netlify'da GitHub repositoriyasini tanlang va deploy qiling.

3. Custom domain o'rnatish uchun Netlify'da "Domain settings" bo'limiga o'ting va o'z domainigizni sozlang.

## Muhim eslatmalar

- Static fayllar `staticfiles_build` papkasida saqlanadi va Netlify tomonidan serverlangan bo'ladi.
- Django API Django + Netlify Functions orqali ishlaydi.
- Ma'lumotlar bazasi sifatida PostgreSQL tavsiya etiladi (Netlify'ga ulanadigan).
- Netlify'ning bepul rejasida API chaqiruvlar soni cheklangan (125k/oy).

## Xatoliklarni bartaraf etish

- Agar deploy vaqtida xatolik yuzaga kelsa, Netlify'ning "Deploys" bo'limida batafsil loglarni ko'rishingiz mumkin.
- Statik fayllar joylanishi bilan bog'liq muammolar bo'lsa `build_files.sh` skriptining to'g'ri ishlashini tekshiring.
- Database xatoliklar bo'lsa, `DATABASE_URL` to'g'ri ekanligini tekshiring. 