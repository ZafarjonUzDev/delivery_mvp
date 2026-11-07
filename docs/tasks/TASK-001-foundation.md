# TASK-001 — Clean Django/PostgreSQL foundation

**Holat:** Codexga yuborish uchun topshiriq, biznes modullarini implementatsiya qilishga ruxsat emas.

## Maqsad

Yangi, bo‘sh `delivery_mvp` repozitoriyda bazaviy Django loyiha skeletini ishga tushirish. Oldingi `delivery_backend` kodini ko‘chirmaslik yoki o‘zgartirmaslik.

## Kirish materiallari

- `docs/decisions.md` — tasdiqlangan qoidalar
- `docs/architecture.md` — taklif etilgan texnik arxitektura
- `docs/database.md` — kelajakdagi DB loyihasi (hozir jadvallarni ko‘chirma)
- `AGENTS.md` — majburiy Codex qoidalari

## Ruxsat etilgan scope

1. Bir dona Django root: `config/`, `apps/`, `templates/`, `static/`, `manage.py` (frontend uchun alohida root yaratma).
2. Ishga tushirishga yetarli dependency management (Python 3.12+, Django 5.2 LTS va mos PostgreSQL adapter; aniq patch versiyalarni o‘zing mos tanla, release versiyalarini taxmin qilma).
3. Dockerfile va Docker Compose: `web` va `db` (PostgreSQL) servicelari; `db` healthcheck; volume; `web` start. Redis, Celery, nginx hozircha kerak emas.
4. `.gitignore` (venv, pycache, `.env`, media, credentials, local DB) va maxfiy qiymatsiz `.env.example`. `SECRET_KEY`, `DEBUG`, `ALLOWED_HOSTS`, DB credentials environmentdan olinadi.
5. Oddiy server-side homepage yoki health check; katalog, buyurtma, savatcha, login, branding va Telegram funksiyasini hozircha yaratma.
6. `accounts` uchun `AUTH_USER_MODEL`ni birinchi migratsiyadan oldin yaratish kerakligini hisobga ol. Minimal `AbstractUser` subclass qabul qilinadigan variant, lekin login identifikatori/telefon maydonlari bo‘yicha noaniqlik paydo bo‘lsa **migrationdan oldin to‘xta va foydalanuvchidan rozilik ol**.
7. Bitta sodda Django smoke test; qaysi buyruqlar ishga tushirilganini va natijalarni ko‘rsat.
8. README’da ishga tushirish va to‘xtatish buyruqlari, test buyruqlari, `.env.example`dan foydalanish yozilsin.

## Scope'dan tashqari

- `Branch`, `Product`, `Order`, `Cart`, `Discount`, `Notification`, `BrandTheme` va biznes modellari.
- DRF API endpointlari, JWT, SMS OTP, Telegram bot/Mini App, to‘lov provayderlari, XLSX export.
- Oldingi repodan biror kodni ko‘chirish; eski repoga push qilish.
- Production serverga deploy, haqiqiy API kalitlari, biznes mijozlarining ma'lumotlari.

## Acceptance criteria

- [ ] Loyiha toza, yangi Git repozitoriyda joylashgan; hujjatlar va AGENTS.md mavjud.
- [ ] Django lokal yoki Docker orqali boshlanadi.
- [ ] PostgreSQL ulanishi ishlaydi yoki qanday tekshirib bo‘lmagani oshkora qayd etiladi.
- [ ] Custom User uchun migration tartibi xavfsiz (eski migrationlar mavjud emas).
- [ ] `python manage.py check` natijasi ko‘rsatilgan.
- [ ] Smoke test natijasi (yoki `not run`) aniq.
- [ ] `.env` Gitga kirmaydi; `.env.example` maxfiy ma'lumotsiz.
- [ ] O‘zgargan/yangi fayllar ro‘yxati va qisqa asos berilgan.
- [ ] Buyruqlar ishlamasa, sabab va keyingi tuzatish taklifi aytiladi.

## Codex yakunidagi hisobot

1. O‘zgargan fayllar va ularning vazifasi.
2. Ishga tushirilgan komandalar, haqiqiy natijalari.
3. Xavfsizlik va migration tekshiruvi.
4. Ochiq savollar.
5. Keyingi eng kichik vazifa: branding foundation (faqat taklif, avtomatik implementatsiya emas).

Foydalanuvchi code review va test natijalarini ko‘rib tasdiqlamaguncha keyingi taskga o‘tma.
