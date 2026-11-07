# Frontend / Web + Telegram Mini App UX arxitekturasi

## UI tamoyillari

- Django Templates SSR + responsive CSS + kichik vanilla JS; frontendni alohida root/paketga ajratmaymiz.
- Web va Mini App aynan bir xil template/data flow ishlatadi. Telegram WebView platform details (safe area, theme, back button) kichik adaptatsiya.
- Dizayn **configurable**: emas faqat rangni o‘zgartirish, balki barcha ekranda yagona dizayn tokenlari, to‘g‘ri kontrast, responsivlik, logo o‘lchami, UI states, fallback image.
- Kategoriyali katalog ovqat va do‘kon uchun umumiy. Product ingredients ixtiyoriy; «Batafsil» universal nom.
- O‘zbek/rus statik matnlarni Django `gettext` bilan, DB mahsulot nom/tavsifni `name_uz/name_ru` bilan.

## Public pages

| URL konsepti | Sahifa | Asosiy vazifa |
|---|---|---|
| `/` | Landing / katalog | Business logo/name, filial, kategoriyalar, featured products, basic contacts |
| `/categories/<slug>/` | Kategoriya | BranchProduct cards: rasm, name, price, availability, `Savatga`, `Batafsil` modal |
| `/cart/` | Savatcha | `+/-`, item summary, discount, branch, total; unavailable item warning |
| `/checkout/` | Checkout | Delivery/pickup, recipient name/phone, geolocation/address if delivery, note, final sum, confirm |
| `/orders/track/<opaque-token>/` | Tracking | Status timeline, no unneeded PII, cancel only NEW |
| `/account/login/` | Optional OTP | Phone, OTP request/verify, account linking |
| `/account/orders/` | Account order history | Auth-only orders and detail |
| `/contacts/` (optional) | Aloqa | Business phone/address, optional Telegram/Instagram; clickable `tel:` |

Product details **modal**: new browser tab yo‘q. Cart focus/scroll preserved; desktop centered dialog, mobile sheet/full-screen; keyboard Escape/close, focus trap, screen-reader labels. Modal JS orqali product endpoint/query bilan populated, mini appda ham shu komponent.

## Admin/dashboard pages

| Sahifa | Amallar |
|---|---|
| `/dashboard/` | Today's NEW orders count, order summaries, pause state |
| `/dashboard/orders/` | Filtered order list and staff status transitions |
| `/dashboard/branches/` | Branch contact, hours, delivery fee/radius, pause per service |
| `/dashboard/catalog/` | Category, Product, BranchProduct pricing/availability, discount |
| `/dashboard/branding/` | Logo, favicon, name, social links, main phone, theme colors, preview/reset |
| `/dashboard/reports/` | By date/branch/status metrics and XLSX export |
| `/dashboard/audit/` | Status and configuration events for authorized users |

**MVP pragmatizmi:** professional custom dashboardning hammasi noldan yozilmaydi. Oddiy CRUD uchun Django Admin, yangi buyurtmalarni ishlash va marketing/branding uchun faqat kerakli maxsus sahifalar.

## Dinamik header/footer

- Desktop header: logo + business name, filial selector, kategoriya, language UZ/RU, savatcha; business phone action.
- Mobile header: logo, filial, cart; overflow/contact menu; ekranni ko‘p tugma bilan to‘ldirmaslik.
- Footer: biznesning aloqa raqamlari, mavjud bo‘lsa Telegram va Instagram, manzil, ish vaqti. `SocialLink.is_visible` + URL check.
- Headerdagi telefon `tel:+998...` normalizatsiya qilingan; Telegram `https://t.me/...`, Instagram `https://www.instagram.com/...` alohida sahifada ochiladi (o‘rinli joyda).
- Logo bo‘lmasa biznes nomi yoki ishlab chiqarilgan neytral placeholder; ijtimoiy havola yo‘q bo‘lsa yashiriladi.

## Theme UI konfiguratsiyasi (taklif)

```text
BrandTheme
  primary_hex       asosiy action
  on_primary_hex    action ichidagi matn
  accent_hex        badge/promo elementlar
  page_bg_hex       sahifa foni
  surface_hex       kartochka/dialog foni
  text_hex          matn
  muted_hex         yordamchi matn
```

Business owner adminida rang tanlash, oldindan ko‘rish (staging yoki CSS preview), kontrast avtomatik baholash, "Restore defaults" bo‘lishi mumkin. Mijozga ranglar faqat tayinlangan CSS variables sifatida beriladi. Barcha joyda doimiy spacing, radius, typographic scale va ikonlar — mahsulot bir professional dizayn oilasida qoladi.

## UX edge states

1. Filial delivery radiusidan tashqari -> boshqa eligible filialni taklif qilish, avtomatik savatchani ko‘chirmaslik.
2. Admin deliveryni pausaga qo‘ydi -> checkout ishlamaydi, cart qoladi, pickup varianti ochiq bo‘lsa taklif.
3. Product out-of-stock -> katalogda disable + matn; cartga oldin tushgan bo‘lsa message, checkoutga block.
4. Narx/discount o‘zgargan -> userga eski/yangi summa va qayta tasdiqlash.
5. NEW 5 daqiqadan oshdi -> mijozga "tasdiq kutilmoqda", buyurtma automatic cancel qilinmaydi.
6. Telegram initData rejected -> foydalanuvchiga qayta ochish/kirish guidance, soxta Telegram status bermaslik.
7. Tarmoq sust -> repeated submitni bloklash, idempotency va error/retry feedback.
8. UZ/RU bo‘sh tarjima -> aniq fallback, noto‘g‘ri encoding bo‘lmasligi.

## Qo‘lda test UX qabul mezonlari

- 360px mobile, tablet, desktop va Telegram WebViewda sahifalar kesilmaydi.
- Buttons only icon bo‘lsa aria-label; focus visible; modal qayta yopilganda fokus oldingi tugmaga qaytadi.
- `Mavjud emas` faqat rang bilan emas, yozuv bilan ham ifodalanadi.
- 4.5:1 matn kontrast (kattada 3:1), zoom 200%da foydalanish mumkin.
- Katalog bir dona produkt/ko‘p produkt, logo yo‘q/logo juda uzun, social links yo‘q/ko‘p holatlarini tekshirish.
- `MINIAPP_ENABLED=false` bo‘lsa webda Telegram miniapp tugmasi ko‘rinmaydi; admin bot messages mustaqil.
