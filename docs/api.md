# Portfolio API Dokumentatsiyasi

## Asosiy Ma'lumot

**API URL:** `https://api.abdulaziz.org.uz/api/`  
**Format:** JSON  
**Autentifikatsiya:** Bearer Token (admin operatsiyalari uchun)

## Endpointlar

### Blog

#### Blog Postlari

**GET** `/api/posts/`

Post koleksiyasini olish.

**Parametrlar:**
- `page` - sahifa raqami (default: 1)
- `page_size` - har bir sahifadagi elementlar soni (default: 10, max: 50)
- `latest` - so'nggi N ta postlarni olish (masalan, `?latest=5`)

**Javob:**
```json
{
  "count": 100,
  "next": "https://api.abdulaziz.org.uz/api/posts/?page=2",
  "previous": null,
  "results": [
    {
      "id": 1,
      "title": "Post sarlavhasi",
      "slug": "post-sarlavhasi",
      "image_url": "https://telegra.ph/file/image.jpg",
      "description": "Post tavsifi markdown formatida",
      "description_html": "<p>Post tavsifi HTML formatida</p>",
      "telegraph_url": "https://telegra.ph/Post-sarlavhasi",
      "views": 150,
      "created_at": "2025-03-29T12:00:00Z",
      "comment_count": 5,
      "absolute_url": "/blog/post-sarlavhasi/"
    }
  ]
}
```

**GET** `/api/posts/{slug}/`

Ma'lum slug bilan postni olish.

**Parametrlar:**
- `sync` - Telegraph bilan sinxronlash (`true` yoki `false`)

**Javob:**
```json
{
  "id": 1,
  "title": "Post sarlavhasi",
  "slug": "post-sarlavhasi",
  "image_url": "https://telegra.ph/file/image.jpg",
  "description": "Post tavsifi markdown formatida",
  "description_html": "<p>Post tavsifi HTML formatida</p>",
  "telegraph_url": "https://telegra.ph/Post-sarlavhasi",
  "views": 150,
  "created_at": "2025-03-29T12:00:00Z",
  "comment_count": 5,
  "absolute_url": "/blog/post-sarlavhasi/"
}
```

**POST** `/api/posts/{slug}/sync_from_telegraph/`

Post kontentini Telegraph dan sinxronlash.

**Javob:**
```json
{
  "success": true,
  "message": "Successfully synced from Telegraph"
}
```

#### Izohlar

**GET** `/api/posts/{slug}/comments/`

Post izohlarini olish.

**Javob:**
```json
[
  {
    "id": 1,
    "name": "Foydalanuvchi",
    "text": "Izoh matni",
    "created_at": "2025-03-29T14:30:00Z"
  }
]
```

**POST** `/api/posts/{slug}/add_comment/`

Postga izoh qo'shish.

**Body:**
```json
{
  "name": "Foydalanuvchi",
  "email": "user@example.com",
  "text": "Izoh matni"
}
```

**Javob:**
```json
{
  "id": 2,
  "name": "Foydalanuvchi",
  "text": "Izoh matni",
  "created_at": "2025-04-04T15:30:00Z"
}
```

### Proyektlar

**GET** `/api/projects/`

Proyektlar koleksiyasini olish.

**Parametrlar:**
- `page` - sahifa raqami (default: 1)
- `page_size` - har bir sahifadagi elementlar soni (default: 10, max: 50)
- `skill` - ko'nikmaga ko'ra filtrlash (masalan, `?skill=python`)
- `featured` - tanlab olingan proyektlarni filtrlash (`?featured=true`)

**Javob:**
```json
{
  "count": 50,
  "next": "https://api.abdulaziz.org.uz/api/projects/?page=2",
  "previous": null,
  "results": [
    {
      "id": 1,
      "title": "Proyekt nomi",
      "slug": "proyekt-nomi",
      "image_url": "https://telegra.ph/file/image.jpg",
      "description": "Proyekt tavsifi",
      "skills": [
        {
          "id": 1,
          "name": "Python",
          "icon_url": "https://telegra.ph/file/icon.jpg",
          "project_count": 15
        }
      ],
      "github_link": "https://github.com/username/project",
      "live_link": "https://project-demo.com",
      "telegraph_url": "https://telegra.ph/Project-01-01",
      "featured": true,
      "views": 120,
      "created_at": "2025-03-29T10:00:00Z",
      "absolute_url": "/projects/proyekt-nomi/"
    }
  ]
}
```

**GET** `/api/projects/{slug}/`

Ma'lum slug bilan proyektni olish.

**Parametrlar:**
- `sync` - Telegraph bilan sinxronlash (`true` yoki `false`)

**Javob:**
```json
{
  "id": 1,
  "title": "Proyekt nomi",
  "slug": "proyekt-nomi",
  "image_url": "https://telegra.ph/file/image.jpg",
  "description": "Proyekt tavsifi",
  "skills": [
    {
      "id": 1,
      "name": "Python",
      "icon_url": "https://telegra.ph/file/icon.jpg",
      "project_count": 15
    }
  ],
  "github_link": "https://github.com/username/project",
  "live_link": "https://project-demo.com",
  "telegraph_url": "https://telegra.ph/Project-01-01",
  "featured": true,
  "views": 120,
  "created_at": "2025-03-29T10:00:00Z",
  "absolute_url": "/projects/proyekt-nomi/"
}
```

**POST** `/api/projects/{slug}/sync_from_telegraph/`

Proyekt kontentini Telegraph dan sinxronlash.

**Javob:**
```json
{
  "success": true,
  "message": "Successfully synced from Telegraph"
}
```

### Ko'nikmalar

**GET** `/api/skills/`

Ko'nikmalar ro'yxatini olish.

**Javob:**
```json
[
  {
    "id": 1,
    "name": "Python",
    "icon_url": "https://telegra.ph/file/icon.jpg",
    "project_count": 15
  }
]
```

**GET** `/api/skills/{id}/projects/`

Ko'nikma bilan bog'liq proyektlarni olish.

**Javob:**
```json
[
  {
    "id": 1,
    "title": "Proyekt nomi",
    "slug": "proyekt-nomi",
    "image_url": "https://telegra.ph/file/image.jpg",
    "description": "Proyekt tavsifi",
    "skills": [
      {
        "id": 1,
        "name": "Python",
        "icon_url": "https://telegra.ph/file/icon.jpg",
        "project_count": 15
      }
    ],
    "github_link": "https://github.com/username/project",
    "live_link": "https://project-demo.com",
    "telegraph_url": "https://telegra.ph/Project-01-01",
    "featured": true,
    "views": 120,
    "created_at": "2025-03-29T10:00:00Z",
    "absolute_url": "/projects/proyekt-nomi/"
  }
]
```

### Telegraph API Integratsiyasi

**GET** `/api/telegraph/page-info/`

Telegraph sahifasi haqida ma'lumot olish.

**Parametrlar:**
- `path` - Telegraph sahifa yo'li (majburiy)

**Javob:**
```json
{
  "success": true,
  "result": {
    "path": "Post-sarlavhasi",
    "url": "https://telegra.ph/Post-sarlavhasi",
    "title": "Post sarlavhasi",
    "description": "Post tavsifi",
    "author_name": "Abdulaziz's Portfolio",
    "content": [...],
    "views": 100,
    "can_edit": true
  }
}
```

**POST** `/api/telegraph/token/`

Telegraph uchun yangi token yaratish. (Faqat admin uchun)

**Body:**
```json
{
  "short_name": "Abdulaziz",
  "author_name": "Abdulaziz"
}
```

**Javob:**
```json
{
  "success": true,
  "access_token": "your-access-token",
  "message": "Token muvaffaqiyatli yaratildi"
}
```

**POST** `/api/telegraph/upload-image/`

Rasmni Telegraphga yuklash.

**Body:**
```
Form data:
- file: (file binary)
```

**Javob:**
```json
{
  "success": true,
  "url": "https://telegra.ph/file/unique-id.jpg",
  "message": "Rasm muvaffaqiyatli yuklandi"
}
```

## Xatolarni qaytarish

**400 Bad Request:**
```json
{
  "success": false,
  "error": "Invalid parameters",
  "message": "Parametrlar noto'g'ri"
}
```

**401 Unauthorized:**
```json
{
  "detail": "Authentication credentials were not provided."
}
```

**404 Not Found:**
```json
{
  "detail": "Not found."
}
```

## Rate Limiting

API so'rovlar chastotasi cheklangan:
- Anonim foydalanuvchilar: 100 so'rov/soat
- Autentifikatsiyalangan foydalanuvchilar: 1000 so'rov/soat

Limitdan o'tib ketganda quyidagi javob qaytariladi:

```json
{
  "detail": "Request was throttled. Expected available in 35 seconds."
}
``` 