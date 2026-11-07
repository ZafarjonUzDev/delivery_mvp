# Qarorlar reyestri — 2026-11-06

## TASDIQLANGAN biznes/scope qarorlari

| ID | Qaror |
|---|---|
| S-00 | Noldan **yangi** Git repozitoriyda toza loyiha boshlanadi. Eski `delivery_backend` kodi asos qilib olinmaydi va o‘chirilmaydi. Ushbu arxiv arxitektura spetsifikatsiyasi, kod emas. |
| S-01 | Yagona white-label kod bazasi; har tadbirkorga alohida backend/frontend konfiguratsiyasi, DB va deployment. Ko‘p filial bitta biznes ichida. |
| S-02 | Web sayt asosiy; Telegram Mini App kodi ham ishlab chiqiladi, tadbirkor uchun **ixtiyoriy** va konfiguratsiya bilan yoqib/o‘chiriladi. Admin Telegram ogohlantirishlari undan mustaqil. |
| S-03 | Katalog, mahsulotlar, savatcha, yetkazib berish va olib ketish, ism/telefon/manzil/lokatsiya, admin buyurtma tasdiqlashi, Telegram ogohlantirishlari, filialga mos narx/mavjudlik — MVP. |
| S-04 | Kuryer paneli, GPS tracking va kuryer tayinlash — MVP emas. |
| BR-11 | Buyurtma qo‘lda tasdiqlanadi; 5 daqiqa `NEW` qolsa **bir marta** Telegram eslatmasi, avtomatik bekor qilinmaydi. |
| BR-12 | Akkauntsiz checkout mumkin; xohlovchi SMS OTP yordamida akkaunt yaratadi/kiradi. |
| BR-14 | Har bir buyurtma uchun qabul qiluvchi ism/telefon va kerakli manzil mustaqil saqlanadi; akkauntli mijozga oldingi ma’lumotlar **taklif etiladi**, tahrirlanadi va har gal tasdiqlanadi. |
| BR-15 | Bitta filialda filial avtomatik; ko‘p filialda mijoz tanlaydi. Radiusdan tashqarida boshqa mos filial taklif etiladi, bo‘lmasa yetkazib bo‘lmasligi va olib ketish ko‘rsatiladi. Radius to‘g‘ri chiziq bo‘yicha aniqlanadi. |
| BR-16 | Har filialda delivery_enabled, lokatsiya, radius va bitta qat’iy delivery_fee. Fee summaga yoki masofaga bog‘liq emas; 0 — bepul. Buyurtmadagi fee snapshot. |
| BR-17 | Filial umumiy ish vaqti, yetkazib berish buyurtma qabul qilish vaqti va olib ketish vaqti alohida, haftalik/jadval bo‘yicha sozlanadi. |
| BR-18 | Har filialda delivery va pickup yangi buyurtmalarini bir-biridan mustaqil pause/resume qilish mumkin. Oldingi buyurtmalar saqlanadi. |
| BR-19 | `NEW` — rad etiladi; `CONFIRMED` va `PREPARING` — mas’ul administrator sabab bilan bekor qiladi; `READY` — faqat biznes egasi/maxsus vakolatli menejer; `COMPLETED`/`CANCELED` yakuniy. |
| BR-20 | Biznes egasi uchun kun/oy/yil/tanlangan vaqt va filial bo‘yicha hisobotlar, audit tarixi va XLSX eksport MVPga kiritiladi. |
| G1.1–G1.5 | Mijoz `NEW`ni bekor qilishi; naqd/terminal tashqi to‘lov; order/payment status alohida; narx snapshot; dublikat checkoutdan himoya. |
| G2.1–G2.6 | Katalog + «Savatga»/«Batafsil»; tafsilotlar modal; `+/-` faqat savatchada; per-filial mavjudlik; butun dona birlik; foiz/summali discount, filial chegirmasi umumiydan ustun, stack yo‘q; uz/ru maydonlar. |
| G3.1–G3.6 | Guest + OTP; Telegram identity serverda tekshirish; hisoblarni ixtiyoriy rozilik + SMS verifikatsiya bilan bog‘lash; persisted cart; filial to‘qnashuvda tanlov; role-based permissions. |
| G4.1–G4.5 | Filtrlangan ko‘rsatkichlar va 3 hisobot turi (buyurtma, mahsulot sotuvlari, bekor qilish), payment bo‘yicha ajratish, status/sozlama auditi, eksport ruxsatlari. |
| UX-01 | Logo, brend ranglari, aloqa telefonlari va ixtiyoriy Telegram/Instagram manzillarini har biznes uchun professional tarzda sozlash **tasdiqlangan**. Aniq model/tokenlar — implementatsiya taklifi. |
| POLICY | Alkogol va tamaki savdosi qo‘llanmaydi. |

## YANGI texnik dizayn takliflari — yakuniy review kutiladi

- `BusinessProfile` (singleton), `BrandTheme` (singleton), `SocialLink` (platform + URL, ixtiyoriy), filial telefonlari ixtiyoriy. Admin orqali preview/reset va rang kontrastini tekshirish.
- Django 5.2 LTS + PostgreSQL + DRF kerakli JSON endpointlar uchun + SSR Django Templates + oz miqdorda JS, Docker Compose.
- Price/discount so‘mda butun son, foiz uchun `Decimal` + `ROUND_HALF_UP` (aniq yaxlitlash texnik qarori reviewda).
- Discount bir vaqtning o‘zida bir nechta mos bo‘lsa: filial scope > tarmoq scope, scope ichida product-specific > umumiy; **bir xil darajadagi takroriy chegirmalar to‘qnashuvini admin validatsiyasi bloklaydi** (reviewda aniqlashtiriladi).
- Mijoz status sahifasi public order ID emas, taxmin qilib topilmaydigan token orqali; tokenning hash qiymati DBda.
- Statuslarni 15–30 soniyada polling, Telegram reminder uchun har 1 daqiqalik scheduler + PostgreSQL notification/outbox, Redis/Celery shart emas.
- Hozircha maxsus soliq/fiskal integratsiya, real to‘lov reconciliatsiyasi, kuryer resurslari yo‘q.

## Tekshiriladigan nozik tafsilotlar

1. Narx chegirmasi qiymatini yaxlitlash va mahsulotga umumiy summa chegirmasi qaysi qatlamda qo‘llanishi.
2. Taklif qilinadigan filialda savatchani almashtirish UX: narxlar o‘zgarganda mijoz tasdiqlaydi, avtomatik ko‘chirmaydi.
3. SMS provayderi, OTP limitlari va abuse-control infratuzilmasi.
4. Role permission matrix: biznes egasi/filial menejeri/admin xizmat vakolatlari.
5. Theme ranglari va logotip o‘lchamlarining dizayn review mezonlari.
6. Cart merge qoidasi, bir checkoutda payment statusni kim va qachon `PAID` qiladi.

Bu bandlar tasdiqlangan xususiyatlarning o‘zini o‘zgartirmaydi, faqat bajarish detallarini aniqlashtirish talab etiladi.
