# Delivery MVP — Codex working agreement

## Purpose

A single reusable white-label Django delivery product for independent restaurant/cafe/fast-food/shop deployments. Web is core; Telegram Mini App optional per deployment. No alcohol or tobacco commerce.

## Hard constraints

1. The user is the approval authority for material business, database, architecture and scope decisions. Read `docs/decisions.md`; never silently override approved rules.
2. Before coding, state exact files affected, goal, scope, acceptance tests and rollback considerations. Do not proceed unless the user approves that task.
3. This is a GREENFIELD project. Start in a clean new Git repository; do not copy, overwrite or refactor the old `delivery_backend` project. Before each task inspect the current NEW repo files and tests and show the proposed diff.
4. No secrets, bot tokens, OTPs, passwords or real customer PII in code, examples or logs. `.env` must not be committed.
5. Prefer simple Django Templates + PostgreSQL + DRF for necessary APIs. Do not add Redis/Celery/WebSocket/microservices just for architectural fashion.
6. Separate tenant deployments/DBs, same main codebase. Brand/theme and contacts are configuration data, not per-customer code forks.
7. Never calculate trusted prices or permissions in browser only. Server must enforce branch access, stock/availability, radius, business hours, discounts and status transitions.
8. Order, OrderItem price and recipient snapshots immutable; changes append status/audit events.
9. Use database transactions and concurrency-safe status transitions/idempotent checkout. Telegram failure must never lose an order.
10. Telegram Mini App identity MUST be server-validated with initData signature and auth_date; do not trust initDataUnsafe. Mini App feature flag must not switch off admin bot alerts.
11. XLSX exports filtered + authorized + logged; sanitize values that might be spreadsheet formula injection.
12. Delivery/pickup pauses are independent; per-branch flat fee may be zero; no courier assignment/tracking.
13. Each task ends with a file-by-file review, commands actually run, test results, known limitations and next small task. Do not claim tests passed unless executed.
14. Respect localization (Uzbek/Russian), responsive UX and WCAG contrast/focus/keyboard basics.

## Document precedence

`docs/decisions.md` (confirmed) > `docs/requirements.md` > `docs/database.md`/`docs/architecture.md`/`docs/api-contract.md`/`docs/frontend-flow.md` (proposed implementation) > task prompt. If conflict arises, STOP and ask the user for a decision.

## Working pace

First Codex task is `docs/tasks/TASK-001-foundation.md`: create only a minimal, testable Django + PostgreSQL foundation, without business-domain models or endpoints. Preserve the user approval gate for every later task. Plan a custom AUTH_USER_MODEL before the initial production migration; do not run migrations against an unknown DB. Gradual, testable commits and explicit user approval at each step.
