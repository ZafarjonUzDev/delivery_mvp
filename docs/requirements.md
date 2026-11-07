# Delivery MVP — Requirements va qabul mezonlari

**Status:** Biznes doirasi tasdiqlangan (G1–G4, BR-11–BR-20); ijro tafsilotlari qarorlar reyestrida ajratilgan.

## Mijoz katalogi / savatcha

- Saytda biznes nomi/logo, kontaktlari, ixtiyoriy ijtimoiy havolalar, uz/ru til tanlash, filial, kategoriya va mahsulotlar ko‘rinadi.
- Har product uchun nom, rasm (bo‘lmasa placeholder), narx, mavjudlik, `Savatga` va `Batafsil`.
- `Batafsil` modal: nom, rasm, tavsif/tarkib (bo‘lsa), narx, mavjudlik, savatga qo‘shish, yopish; klaviatura/telefon bilan ishlaydi.
- `+/-` faqat savatchada; miqdor butun son va >=1, 0 bo‘lsa item olib tashlanadi.
- Savatcha bitta filialga bog‘lanadi; filial almashtirilganda mavjudlik va narx qayta tekshiriladi, o‘zgarish haqida rozilik olinadi.
- Anonymous cart Django session bilan, registered cart User bilan saqlanadi; login merge noaniq bo‘lsa tanlash so‘raladi.
- Checkout server-side recalculation qiladi, ikki marta yuborilgan request duplicate orderga aylanmaydi.

**Qabul mezonlari:** mavjud bo‘lmagan mahsulotni qo‘shib bo‘lmaydi; modal yopilganda katalog joyi saqlanadi; guest cart sessiya davomida saqlanadi; narx o‘zgargan bo‘lsa oldingi summa tasdiqlanmasdan checkout yakunlanmaydi.

## Buyurtma / qabul qiluvchi / filial

- Guest checkout mumkin; buyurtma qabul qiluvchining ismi va aloqa telefoni har gal tasdiqlanadi, oldingi ma’lumotlar login qilinganda prefill bo‘ladi.
- Delivery uchun lokatsiya nuqtasi va qo‘shimcha matnli manzil ishlatiladi; xaritada belgilash yoki ruxsatli geolokatsiya imkoniyati; nuqta mavjud bo‘lmasa radius avtomatik tasdiqlanmaydi.
- Pickup uchun mijoz lokatsiyasiga radius cheklovi yo‘q.
- Bitta filial bo‘lsa avtomatik; ko‘p filialli biznesda mijoz filial tanlaydi.
- Har filialning delivery fee (0 ham), delivery radius, koordinata, ish vaqti, delivery/pickup pauza holatlari alohida.
- Radiusdan tashqarida boshqa mos filial ko‘rsatiladi; bo‘lmasa delivery rad etiladi va pickup taklif etiladi.
- Buyurtma `NEW` bo‘ladi, admin qo‘lda tasdiqlaydi, 5 daqiqa `NEW` qolsa bir martalik Telegram reminder, avtomatik cancel yo‘q.
- `NEW` customer cancellation mumkin; `CONFIRMED`, `PREPARING` uchun maxsus vakolat; `READY` owner/delegated manager; `COMPLETED` yakuniy.
- Checkoutdagi nom, telefon, delivery manzili, discount, unit price, delivery fee va total immutable snapshot sifatida saqlanadi.

**Qabul mezonlari:** buyurtma mavjud bo‘lmagan xizmat vaqtida yaratilmaydi; pauzadagi xizmat checkout rad etiladi; 5-min eslatma faqat hanuz `NEW` bo‘lsa bitta marta rejalashtiriladi; istalgan sabab bilan Telegram ishlamasa Order DBda qoladi.

## Account / Telegram Mini App

- Web: session + ixtiyoriy SMS OTP; SMS raqam tasdiqlanmaguncha verified deb ko‘rsatilmadi.
- Telegram initData serverda HMAC/signature tekshiruvi + auth_date TTL; Telegram ID o‘z-o‘zidan telefon raqami emas.
- Web va Telegram akkauntlarini birlashtirish mijoz roziligi va SMS orqali telefon egaligini tekshirishdan keyin; merged cart mantiqli va ko‘rinadigan bo‘lsin.
- Mini App tadbirkor uchun optional. `MINIAPP_ENABLED=false` bo‘lsa Telegram ichidagi mijoz authorization endpointlari bloklanadi, admin Telegram alertlar esa ishlayveradi.
- Guest tracking tokenli maxfiy sahifada status ko‘radi, id taxmin qilish bilan boshqa odam buyurtmasi ochilmaydi.

**Qabul mezonlari:** noto‘g‘ri initData 401; boshqa mijozning order IDsi shaxsiy ma’lumot ochmaydi; Mini App OFF holatda web checkout va admin alertlar ishlaydi.

## Hisobotlar / audit / eksport

- Filial, sana oralig‘i, status bo‘yicha buyurtmalar, sotilgan mahsulotlar va bekor qilishlar hisobotlari.
- `COMPLETED` qiymati va `PAID` qiymati alohida (real bank hisob-kitobi emas, tizimda qayd qilingan summa).
- Owner va vakolatli manager eksport qiladi; xodim role ruxsatidan ortiq ma’lumotga kira olmaydi.
- XLSX eksportlar shaxsiy ma’lumotlarni defaultda cheklaydi; formula injection himoyasi va audit log.
- Buyurtma statusi, cancel, branch sozlamalari, discount, mahsulot narxi, branding konfiguratsiyasi kabi muhim amallar vaqt/actor/before-after bilan auditda saqlanadi.

**Qabul mezonlari:** boshqa filial buyurtmasi ko‘rinmaydi; hisobot total order snapshotlarga mos; exportga ruxsatsiz so‘rov 403; cancel sababi va actor tarixdan aniqlanadi.

## White-label theme va biznes kontaktlari

- Har biznes uchun `BusinessProfile` nomi, telefon, qo‘shimcha telefon, Telegram/Instagram havolalari, aloqa manzili va logosi.
- `BrandTheme`: primary, on_primary, accent, page_bg, surface, text, muted kabi cheklangan dizayn tokenlari. Admin rangni validatsiya bilan sozlaydi, oldindan ko‘rish va defaultga qaytarish mumkin.
- Header: biznes nomi/logo va savatcha; asosiy kontakt tugmasi; footer: telefon, manzil, faqat mavjud social linklar. Mobil interfeysda barchasi chiqmasin — moslashuvchan joylashuv.
- Web va Mini App **bir xil theme** va brendingdan foydalanadi, lekin Mini App uchun Telegram WebView spacing/safe areas moslanadi.
- Brend sozlamalari bir biznes DBsi doirasida qoladi; admin CSS/JS skriptni o‘zboshimchalik bilan kirita olmaydi.

**Qabul mezonlari:** logo/ranglar almashganda boshqa biznes deploymentiga ta’sir qilmaydi; fon va matn kontrasti tekshiriladi; noto‘g‘ri URL/xavfli fayl rad etiladi; social URL bo‘lmasa tugma chiqmaydi; favicon/alt matn/SEO title brendga mos.
