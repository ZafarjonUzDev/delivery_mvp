# Delivery MVP — Clean Foundation

**Holat:** TASK-001 doirasidagi minimal Django + PostgreSQL poydevori. Bir dona Django ildizi, serverda render qilinadigan homepage, static CSS, custom User va smoke test mavjud. Docker Compose mahalliy ishlab chiqish uchun; production deploy bu vazifaga kirmaydi.

**Maqsad:** restoran, kafe, fast-food va do‘kon uchun alohida o‘rnatiladigan, bir kod bazali web ordering + ixtiyoriy Telegram Mini App. `docs/decisions.md` ichidagi tasdiqlangan qoidalar o‘z kuchida; kelajakdagi biznes modullari hozircha implementatsiya qilinmagan.

## Muhit va tuzilma

- Docker Engine va Docker Compose v2, secretlarni mahalliy yaratish uchun Python 3.
- Container versiyalari: Python `3.12.16-slim-bookworm`, PostgreSQL `17.11-bookworm`.
- Python bog‘liqliklari: Django `5.2.19`, psycopg `3.3.8`; aniq paketlar `requirements.txt`da.
- `config/`, `apps/`, `templates/`, `static/`, `manage.py` — yagona Django loyiha ildizi; `tests/` — smoke test.
- Compose loyihasi `delivery-mvp-foundation`; `web` va `db` servicelari. PostgreSQL ma’lumotlari loyiha prefiksli `postgres_data` volumeda saqlanadi. DB porti hostga ochilmaydi; web faqat `127.0.0.1` orqali ochiladi.

## Birinchi mahalliy sozlash

Quyidagi buyruqlarni shu repozitoriy ildizida bajaring. `cp` buyrug‘i faqat `.env` hali mavjud bo‘lmaganda bajariladi; mavjud konfiguratsiyani ustidan yozmang.

```bash
cp .env.example .env
python3 - <<'PY'
from pathlib import Path
import secrets

env_path = Path(".env")
generated = {
    "SECRET_KEY": secrets.token_urlsafe(64),
    "POSTGRES_PASSWORD": secrets.token_urlsafe(48),
}
lines = []
for line in env_path.read_text().splitlines():
    key, separator, value = line.partition("=")
    if key in generated and separator and not value.strip():
        line = f"{key}={generated[key]}"
    lines.append(line)
env_path.write_text("\n".join(lines) + "\n")
env_path.chmod(0o600)
PY
```

Script secretlarni terminalga chiqarmaydi; mavjud bo‘sh bo‘lmagan qiymatlarni saqlaydi. `.env` Git va Docker build kontekstidan chiqarilgan. Uni ulashmang va logga chiqarmang. `.env.example`da `SECRET_KEY` va `POSTGRES_PASSWORD` ataylab bo‘sh: ular berilmasa Compose ishga tushmaydi.

Mahalliy standartlar: `DEBUG=true`, `ALLOWED_HOSTS=localhost,127.0.0.1,[::1]`, `POSTGRES_DB=delivery_mvp`, `POSTGRES_USER=delivery_mvp`, `WEB_PORT=8000`. Container ichida DB hosti `db`, porti `5432`. Bular mahalliy muhit sozlamalari; haqiqiy mijoz ma’lumotlari yoki production credentiallardan foydalanmang.

## Birinchi ishga tushirish va migratsiya

Avval konfiguratsiyani qiymatlarini chop etmasdan tekshiring, image yarating va DB healthcheck tugashini kuting:

```bash
docker compose config --quiet
docker compose build
docker compose up -d --wait db
```

Bu loyiha uchun yangi, alohida DB ishlatilayotganini tekshiring. Birinchi migratsiyadan oldin quyidagi so‘rov **0 qator** qaytarishi kerak:

```bash
docker compose exec -T db sh -c 'exec psql -v ON_ERROR_STOP=1 --username="$POSTGRES_USER" --dbname="$POSTGRES_DB"' <<'SQL'
SELECT schemaname, tablename
FROM pg_tables
WHERE schemaname NOT IN ('pg_catalog', 'information_schema')
ORDER BY schemaname, tablename;
SQL
```

Agar jadval mavjud bo‘lsa yoki volume kelib chiqishi noma’lum bo‘lsa, birinchi migratsiyani boshlamang. Mavjud DBni o‘chirmasdan uning qaysi loyihaga tegishli ekanini aniqlang. Avval aynan shu foundation uchun yaratilgan DB qayta ishga tushirilganda jadvallar mavjudligi kutiladi; uni bo‘shatish kerak emas.

Faqat tasdiqlangan yangi DBda migratsiya rejasini ko‘rib, keyin qo‘llang:

```bash
docker compose run --rm web python manage.py migrate --plan
docker compose run --rm web python manage.py migrate
docker compose up -d web
```

Homepage: <http://127.0.0.1:8000/> (`WEB_PORT` o‘zgarsa mos portni ishlating). Web Django development serverida ishlaydi. Startup avtomatik migratsiya bajarmaydi. Keyingi oddiy ishga tushirish: `docker compose up -d`.

Kod image ichiga nusxalanadi; kod o‘zgargach `docker compose build web` va `docker compose up -d web` bilan qayta yarating.

`AUTH_USER_MODEL = "accounts.User"` dastlabki migratsiyadan oldin o‘rnatilgan; `accounts.User` minimal `AbstractUser` subclass. Bu mijoz login identifikatorini yakuniy tanlash emas: telefon maydonlari, SMS OTP, login sahifasi va Telegram identity keyingi alohida tasdiqlanadigan vazifalarga qoldirilgan. Eski loyihaning kodi yoki migratsiyalari ko‘chirilmagan.

## Tekshirish

```bash
docker compose exec web python manage.py check
docker compose exec web python manage.py makemigrations --check --dry-run
docker compose exec web python manage.py test
curl --fail --silent --show-error http://127.0.0.1:8000/
curl --fail --silent --show-error http://127.0.0.1:8000/static/css/base.css
```

Smoke test PostgreSQLda vaqtinchalik test DB yaratadi va o‘chiradi; custom User, parolsiz test foydalanuvchi va homepage/template/static havolasini tekshiradi. Testdagi sun’iy username haqiqiy mijoz ma’lumoti emas. Yuqoridagi buyruqlar ishga tushirish yo‘riqnomasi; ularning amaldagi natijalari TASK-001 yakuniy hisobotida beriladi.

## Muhit yoki build xatosi bo‘lsa

Compose host shell environment qiymatlarini `.env`dan ustun oladi. Masalan, hostdagi `DEBUG=release` Django uchun yaroqsiz va startup uni rad etadi. Bunday muhitda `.env`dagi qiymatni ishlatish uchun Compose buyruqlariga `env -u DEBUG` prefiksini qo‘shing:

```bash
env -u DEBUG docker compose run --rm web python manage.py check
env -u DEBUG docker compose up -d web
```

Ayrim Docker Compose `2.40.3` muhitlarida build Dockerfile bajarilishidan oldin `doBuildBake` / `slice bounds out of range` xatosi bilan to‘xtashi mumkin. Shu host xatosi uchun muqobil buyruq:

```bash
COMPOSE_BAKE=false docker compose build web
```

Muqobil builder eskirish haqida ogohlantirish chiqarishi mumkin. Compose/Buildx yangilash bu vazifaga kirmaydi; image build tugagach odatdagi DB va web buyruqlarini davom ettiring.

## To‘xtatish va qayta ko‘rib chiqish

```bash
docker compose down
```

Bu buyruq container va Compose tarmog‘ini to‘xtatadi, PostgreSQL volumesini saqlaydi. Rollback ko‘rib chiqishda avval shu buyruq bilan muhitni to‘xtating va kod o‘zgarishlarini tekshiring; DB yoki volumeni o‘chirish TASK-001 yo‘riqnomasiga kirmaydi. `.env`dagi DB credentialini mavjud volume yaratilgandan so‘ng o‘zgartirish PostgreSQL ichidagi credentialni avtomatik o‘zgartirmaydi.

## Hujjatlar va tasdiqlangan chegaralar

1. [Qarorlar reyestri](docs/decisions.md) — tasdiqlangan qarorlar va ochiq texnik tafsilotlar.
2. [Talablar](docs/requirements.md) — funksional talablar va qabul mezonlari.
3. [DB loyihasi](docs/database.md) — kelajakdagi ERD, constraint va indexlar.
4. [Arxitektura](docs/architecture.md) — Django modullari, xizmat chegaralari, xavfsizlik, deploy.
5. [Frontend oqimi](docs/frontend-flow.md) — responsive UX, brend va tillar.
6. [API loyihasi](docs/api-contract.md) — keyingi API va autentifikatsiya takliflari.
7. [Implementatsiya rejasi](docs/implementation-plan.md) — bosqichlar va tasdiq chegaralari.
8. [TASK-001](docs/tasks/TASK-001-foundation.md) va [AGENTS.md](AGENTS.md) — joriy scope va ish qoidalari.
9. [Tizim diagrammasi](diagrams/system.mmd) va [ERD](diagrams/erd.mmd) — Mermaid diagrammalari.

- Har biznes alohida deployment va DBda; bir biznesning ko‘p filiali shu deployment ichida. Barcha deploymentlar bir asosiy kod bazasidan foydalanadi.
- Eski `delivery_backend` loyihasiga tegilmaydi. Git commit va push TASK-001 doirasida bajarilmaydi.
- Hozircha katalog, filiallar, buyurtma, savatcha, branding, chegirma, API, OTP, Telegram, to‘lov yoki eksport logikasi yo‘q.
- Kuryer boshqaruvi, GPS va avtomatik kuryer tayinlash MVPga kirmaydi. Alkogol va tamaki savdosi qo‘llanmaydi.
- Keyingi vazifa faqat foydalanuvchi code review va natijalarni ko‘rib tasdiqlagandan so‘ng boshlanadi. Eng kichik keyingi taklif — branding foundation; bu README uni bajarishga ruxsat bermaydi.

Rasmiy texnik manbalar: [Django custom User](https://docs.djangoproject.com/en/5.2/topics/auth/customizing/), [Telegram Mini Apps](https://core.telegram.org/bots/webapps), [WCAG 2.2](https://www.w3.org/TR/WCAG22/).
