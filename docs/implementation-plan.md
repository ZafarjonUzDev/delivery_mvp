# Codex Implementation Plan — bosqichma-bosqich, approval-gated

**Status:** GREENFIELD — yangi repozitoriy noldan boshlanadi. Ishlar kichik tasklar va foydalanuvchi tasdig‘i bilan bajariladi. Eski `delivery_backend` kodini import qilish yoki o‘zgartirish taqiqlanadi.

## Phase 0 — Greenfield documentation handoff

**Maqsad:** bo‘sh yangi Git repozitoriy yaratish, mavjud arxitektura hujjatlarini yangi repoga joylash, hech qanday eski kodni ko‘chirmaslik.
**Scope:** `docs/`, `diagrams/`, `AGENTS.md`, README; keyingi vazifa `docs/tasks/TASK-001-foundation.md`.
**Accept:** yangi repozitoriyda eski loyiha fayllari yo‘q; `docs/decisions.md`da tasdiqlangan qarorlar saqlangan.

## Phase 1 — Foundation (yangi, toza repository)

**Prereq:** greenfield tanlangan; `docs/decisions.md` va `AGENTS.md` o‘qilgan.
**Maqsad:** minimal Django projekti + PostgreSQL + Docker Compose + env sozlamalari + smoke test. Custom User birinchi migratsiyadan oldin tayyor bo‘lishi shart; tafsilot tasdiqlanmaguncha migration boshlanmaydi.
**Scope:** `TASK-001-foundation.md`; hech qanday Catalog/Branch/Order/Telegram/business logic yaratilmaydi.
**Accept:** yangi `delivery_mvp` repozitoriy, `check`, server startup, DB connection va smoke test amalda tekshirildi; `.env` Gitga kiritilmadi.

## Phase 1b — Branding (alohida tasdiq bilan)

**Maqsad:** `BusinessProfile`, `BrandTheme`, `SocialLink`ni yaratish.
**Accept:** default brand bilan homepage render, business name/logo/phone/icons optional, color validation, upload validation, theme preview/reset; migrations reversible; lint + Django check + model tests.

## Phase 2 — Branch, schedule & catalog

**Maqsad:** Branch, BranchHours, Category, Product, BranchProduct va filial filterlari.  
**Accept:** 1 filial auto, ko‘p filial qo‘lda; fee=0 mumkin; pause va interval soatlari; radius test cases, next-day schedule; branch price + availability UI.

## Phase 3 — Cart and checkout core

**Maqsad:** session/User cart, quantity only cart, per-branch cart, checkout snapshots and idempotency.  
**Accept:** guest/registered carts, merge conflict display, 409 price change, invalid location refusal, duplicate submit single order, total server calculated. PostgreSQL transaction tests.

## Phase 4 — Order status/notifications

**Maqsad:** permissioned status transitions, NEW/CONFIRMED/PREPARING/READY/COMPLETED/CANCELED, status history, Telegram new order + one reminder at 5min.  
**Accept:** READY cancel only owner/delegated manager; reason audit; one reminder, no auto cancel; failure Telegram no lost order; two staff concurrency test.

## Phase 5 — OTP + Telegram Mini App (optional)

**Maqsad:** SMS OTP opt-in accounts, session auth, validated initData, linking with consent and verified phone.  
**Accept:** guest web works, Mini App ON works, Mini App OFF truly disables auth while admin Telegram alerts stay ON; no unauthenticated access to other users' cart/orders.

## Phase 6 — Discounts, reports, audit, XLSX

**Maqsad:** fixed/percent discounts with branch precedence, owner reports, status/config audit and 3 XLSX reports.  
**Accept:** correct discount ordering, no negative total, statuses and payment independent, branch isolation, audit append-only, formula-injection-safe export, bounded filtered queries.

## Phase 7 — Production readiness & pilot

**Maqsad:** security, deployment, backup, media handling, responsive UX, prod settings, docs, CI checks.  
**Accept:** tests actually run + logs, `check --deploy`, TLS, secure cookies, `.env` outside repo, restore tested, one business pilot flow success, Web + Mini App ON/OFF regression.

## General Definition of Done (DoD)

- Faqat oldindan tasdiqlangan scope; talab o‘zgarsa yangi qaror so‘raladi.
- Security: permissions, input validation, PII protection, CSRF, branch isolation, race conditions.
- Unit + integration tests (PostgreSQLda), migration review, rollback consideration.
- Code review diff (file-by-file), validatsiya buyruqlari va haqiqiy natijalar (executed vs not executed ajratilgan).
- User mantig‘ini tushunganidan va ochiq rozilik berganidan keyin task yopiladi.

## Birinchi Codex vazifasi

`docs/tasks/TASK-001-foundation.md` ichidagi topshiriqdan foydalaning. U faqat ishlaydigan minimal infratuzilma va smoke test yaratadi; hech qanday biznes qoidalarini kodlamaydi.
