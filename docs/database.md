# PostgreSQL ma’lumotlar modeli — ERD V1.0 (draft)

**Maqsad:** biznes qoidalarni migratsiya yozishdan oldin izchil ma’lumot modeliga aylantirish. ERD `../diagrams/erd.mmd` da. **Bu yakuniy migration emas; NULL, ON DELETE, Decimal aniqligi reviewda tekshiriladi.**

## Model nomlari va asosiy maydonlar

Barcha jadvallarda odatda `id BIGINT PK` yoki kerakli joyda `UUID PK`, `created_at timestamptz`, `updated_at timestamptz` bo‘ladi. Pul qiymatlari **UZS butun so‘m** sifatida `BIGINT`da; hisoblashlar serverda `Decimal` orqali va chekli yaxlitlash bilan bajariladi. JSONB faqat audit oldingi/keyingi ma’lumotlarida, asosiy biznes jadvallari normalizatsiya qilingan.

### A. Branding (`branding` app)

| Jadval | Muhim maydonlar | Qoida / index |
|---|---|---|
| `BusinessProfile` | `id`, `name_uz`, `name_ru`, `short_name`, `business_kind`, `phone_primary`, `phone_secondary?`, `contact_address_uz?`, `contact_address_ru?`, `logo?`, `favicon?`, `is_active` | Bir deploymentda bitta faol profil (singleton invariant). `business_kind` faqat ko‘rsatish/katalog moslashuvi; biznes qoidasini kodga if bilan sochib yubormaydi. |
| `BrandTheme` | `business_id` (OneToOne), `primary_hex`, `on_primary_hex`, `accent_hex`, `page_bg_hex`, `surface_hex`, `text_hex`, `muted_hex`, `updated_by_id?` | Hex regex/format validatsiya, contrast tekshiruv, default theme, audit. Erkin CSS saqlanmaydi. |
| `SocialLink` | `business_id`, `platform` (TELEGRAM, INSTAGRAM, WEBSITE), `url`, `is_visible`, `sort_order` | `unique(business,platform)` MVP; faqat `https`; platform hostlari tekshiriladi. |

`phone_primary` biznesning aloqa telefoni; filialga alohida kontakt uchun `Branch.contact_phone?`. Social linklar header/footer/kontaktda markazlashgan; avtomatik `target=_blank` + `rel=noopener noreferrer`.

### B. Accounts & access (`accounts` app)

| Jadval | Muhim maydonlar | Qoida / index |
|---|---|---|
| `User` | `id`, `phone?`, `is_phone_verified`, `is_active`, `first_name?`, `last_name?`, `is_staff` | `AUTH_USER_MODEL` birinchi migratsiyada. Verifikatsiyalangan telefon unique; Telegram-only uchun `phone=NULL` mumkin; password unusable bo‘lishi mumkin. |
| `TelegramIdentity` | `id`, `user_id`, `telegram_user_id`, `linked_at` | unique telegram ID, OneToOne user (bir biznes uchun). `initData` tekshiruvsiz yozilmaydi. |
| `OTPChallenge` | `id`, `phone`, `code_digest`, `expires_at`, `consumed_at?`, `attempts`, `purpose`, `request_ip_hash?` | OTP ni ochiq saqlamaslik, urinish/time limit, bir martalik consumption, requested_by NULL bo‘lishi mumkin. |
| `StaffMembership` | `id`, `user_id`, `branch_id?`, `role` (OWNER/MANAGER/STAFF), `is_active` | Ownerning global scope’i biznes kontekstida, menejerga bir nechta filial delegatsiyasi mumkin. `unique(user, branch, role)` (NULL branch owner uchun alohida partial unique). Huquqlar server-side. |

**Review:** Userning customer/staff rollenini bir modelda ushlash soddaroq; CustomerProfile faqat keyinchalik qo‘shimcha preference kerak bo‘lsa. Guestda User yo‘q, buyurtma `user_id=NULL`.

### C. Branch & catalog (`branches`, `catalog`)

| Jadval | Muhim maydonlar | Qoida / index |
|---|---|---|
| `Branch` | `id`, `business_id`, `name_uz`, `name_ru`, `address_uz`, `address_ru`, `contact_phone?`, `latitude`, `longitude`, `is_active`, `delivery_enabled`, `pickup_enabled`, `delivery_paused`, `pickup_paused`, `delivery_fee_uzs`, `delivery_radius_km` | `fee>=0`, `radius>0` (delivery enabled holatda), `lat [-90,90]`, `lng [-180,180]`; `index(business,is_active)` |
| `BranchHours` | `id`, `branch_id`, `weekday 0..6`, `service_type` (BRANCH/DELIVERY/PICKUP), `opens_at`, `closes_at`, `is_closed`, `starts_previous_day?` emas | Bir kundagi ko‘p intervalga ruxsat; tun kesish holatini xizmat orqali tekshirish; `(branch, weekday, service_type, opens_at)` index; interval overlap validatsiyasi service qatlamida. |
| `Category` | `id`, `name_uz`, `name_ru`, `slug`, `sort_order`, `is_active` | unique slug; kategoriya umumiy, mahsulot filiallarga bog‘liq. |
| `Product` | `id`, `category_id`, `name_uz`, `name_ru`, `description_uz?`, `description_ru?`, `ingredients_uz?`, `ingredients_ru?`, `image?`, `unit` (PIECE), `is_published`, `sort_order` | Tarmoq mahsulot ta’rifi; mahsulot olib tashlansa oldingi OrderItem snapshotlari qoladi. |
| `BranchProduct` | `id`, `branch_id`, `product_id`, `price_uzs`, `is_available`, `is_active`, `max_per_order?` | `unique(branch, product)`, `price>=0`, `max_per_order>0`; per-filial narx va availability. |
| `Discount` | `id`, `branch_id?`, `product_id?`, `type` (PERCENT/FIXED), `value`, `starts_at?`, `ends_at?`, `is_active` | branch NULL=tarmoq; product NULL=shu scope barcha mahsuloti; branch specific ustun; stacked emas; konfliktdagi aksiyalarni admin validation bilan bloklash. |

**Discount hisoblash — tasdiqlangan asos + aniqlashtiriladigan qatlam:** filial chegirmasi > global chegirma; stack yo‘q. 0%..100%, FIXED unit price dan katta bo‘lmasligi, yakuniy narx >=0. Bir xil scope ichida bir nechta aksiya ustuvorligi qoidasi reviewda. Boshlanish va tugash vaqti Asia/Tashkent foydalanuvchi mintaqasiga mos aks ettiriladi, DB `timestamptz`.

### D. Savatcha va buyurtma (`carts`, `orders`)

| Jadval | Muhim maydonlar | Qoida / index |
|---|---|---|
| `Cart` | `id`, `user_id?`, `session_key?`, `branch_id`, `is_active`, `updated_at` | User yoki session; guest cart sessionga; bitta aktiv cart scope qoidasi service qatlamida. |
| `CartItem` | `id`, `cart_id`, `branch_product_id`, `quantity` | `unique(cart,branch_product)`, `quantity>0`; cart.branch = branch_product.branch server validation. |
| `Order` | `id`, `public_number`, `tracking_token_hash`, `user_id?`, `branch_id`, `fulfillment_type` (DELIVERY/PICKUP), `status`, `payment_method` (CASH/TERMINAL), `payment_status` (UNPAID/PAID), `recipient_name`, `recipient_phone`, `address_text?`, `latitude?`, `longitude?`, `customer_note?`, `subtotal_uzs`, `discount_uzs`, `delivery_fee_uzs`, `total_uzs`, `idempotency_key`, `cancellation_type?`, `cancellation_reason?`, `cancellation_note?`, `canceled_by_id?`, `canceled_at?`, `created_at`, `updated_at` | Public ID unique; token salt/hash (hech qachon taxmin qilinadigan order idni auth o‘rniga ishlatmaslik); `idempotency_key` unique scope. `total=subtotal-discount+fee`, payment PAID alohida. |
| `OrderItem` | `id`, `order_id`, `product_id?`, `name_uz_snapshot`, `name_ru_snapshot`, `unit_price_uzs`, `discount_per_unit_uzs`, `quantity`, `line_total_uzs` | `quantity>0`, `line_total>=0`, immutable snapshots; order items kamida 1. |
| `OrderStatusHistory` | `id`, `order_id`, `from_status?`, `to_status`, `actor_user_id?`, `action`, `reason?`, `created_at` | append-only; `index(order,created_at)`; guest cancel actor_type token via audit text (identity disclosure qoidasi). |
| `PaymentHistory` (minimal) | `id`, `order_id`, `old_status`, `new_status`, `actor_user_id`, `created_at` | `PAID` holatini qo‘lda o‘zgartirish ham audit qilinadi; gateway yo‘q. |

**Ruxsat etilgan order statuslar:** NEW -> CONFIRMED -> PREPARING -> READY -> COMPLETED; NEW -> CANCELED (mijoz/admin); CONFIRMED, PREPARING -> CANCELED (vakolatli admin); READY -> CANCELED (owner/authorized manager); COMPLETED/CANCELED terminal. Adminning `PAID` belgilashi status lifecycle’dan mustaqil. Qayta ikki buyurtma yaratmaslik uchun `idempotency_key` tranzaksiya bilan tekshiriladi. Mijozga tracking token aniq tasodifiy, yetarlicha kuchli; DBda faqat hash.

### E. Notifications & reports (`notifications`, `audit`, `reports`)

| Jadval | Muhim maydonlar | Qoida / index |
|---|---|---|
| `Notification` | `id`, `order_id`, `type` (NEW_ORDER/REMINDER_5M), `scheduled_at`, `status` (PENDING/SENDING/SENT/FAILED/SKIPPED), `attempts`, `next_retry_at?`, `sent_at?`, `last_error_code?` | `unique(order,type)` (5 min reminder faqat 1 ta); `index(status,scheduled_at)`. Telegram ishlamasa order yaratishga xalaqit yo‘q. |
| `AuditEvent` | `id`, `actor_user_id?`, `entity_type`, `entity_id`, `action`, `changes_before_json?`, `changes_after_json?`, `branch_id?`, `ip_hash?`, `created_at` | append-only, maxfiy maydonlar maskirovka; `index(entity_type,entity_id,created_at)`; `index(branch_id,created_at)`. |
| `ExportAudit` | `id`, `actor_user_id`, `report_type`, `filters_json`, `exported_row_count`, `created_at` | Faqat vakolatli role; eksport logi append-only. |

Hisobotlar uchun dastlab alohida summary table shart emas: `Order`/`OrderItem`/history dan indexed ORM aggregation ishlatiladi. Katta hajmga chiqqanda materialized view/cache faqat o‘lchov natijasiga qarab qo‘shiladi.

## Foreign keys va ON DELETE

- `OrderItem` snapshot ma’lumotlari saqlanadi; `product_id` `SET_NULL`, order deletion esa odatiy admin actiondan taqiqlanadi.
- `Order` -> `Branch` PROTECT; `Branch` arxivlanadi (`is_active=False`), o‘chirilmaydi, agar order bo‘lsa.
- `Order` -> `User` SET_NULL bilan shaxsiy akkauntni o‘chirish protokoli review qilinadi; audit va retention siyosati alohida.
- `BrandTheme` -> `BusinessProfile` CASCADE faqat deploymentni boshidan olib tashlash tartibi doirasida.
- `CartItem` -> `Cart` CASCADE; `CartItem` -> `BranchProduct` PROTECT (aktiv cartlarni revalidate).
- `OrderStatusHistory` -> `Order` PROTECT, ruxsat bilan audit tarixini saqlash.

## DB constraint va index checklist

1. `unique(branch_id, product_id)` BranchProduct; `unique(cart_id, branch_product_id)` CartItem; `unique(order_id, notification_type)` Notification.
2. `CHECK fee >= 0`, `price >=0`, `quantity>0`, `radius >0`, `lat/lng range`; `discount.value` type ga mos.
3. `INDEX orders(branch_id, created_at DESC)`, `orders(status, created_at DESC)`, `orders(payment_status, created_at DESC)`; `orders(user_id, created_at DESC)`.
4. `INDEX branch_product(branch_id,is_active,is_available)`; `discount(branch_id,product_id,is_active,starts_at)`.
5. `UNIQUE order.public_number`, `UNIQUE order.idempotency_key` (global UUID bo‘lsa), `UNIQUE telegram_identity.telegram_user_id`.
6. `UNIQUE active registered phone`, `nullable` telefonlar uchun partial unique yoki Django/Postgres NULL semantics.
7. Status `choices` application validation bilan, kerak bo‘lsa DB CHECK; transaction va lock order statusda.
8. Ikki scheduler bir notificationni olib yubormasligi uchun `select_for_update(skip_locked=True)` va claim state ishlatish; Telegram ACK yo‘qolishida 2 marta xabar ketishi mumkinligi qayd etiladi.

## Migration va verifikatsiya tartibi

1. Birinchi migration: `accounts.User` (agar repositoryda allaqachon migratsiya bor bo‘lsa, to‘xtash, mavjud kodni tahlil qilish; avtomatik almashtirmaslik).
2. `branding`, `branches`, `catalog` keyin `carts`, `orders`; so‘ng `notifications`, `reports`, `audit`.
3. `makemigrations --check --dry-run`, `migrate --plan`, `check`, PostgreSQL integratsion testlar.
4. Snapshot/cancel/history/order duplicate, role isolation, no-PII export, discount priority, radius edge va overnight schedule testlari.
