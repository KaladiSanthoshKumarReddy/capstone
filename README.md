# Capstone — AI-Driven SDLC with Human-in-the-Loop

> **Group:** mm-learning-group-1 | **Project:** EPMCDMETST | **Branch:** `main`

A brownfield React + Node.js task-management app used to demonstrate a full AI-assisted Software Development Lifecycle (SDLC) powered by **Claude Code CLI** via **CodeMie**. Every phase — from BA analysis through deployment — is driven by specialised Claude agents with Human-in-the-Loop checkpoints.

---

## Live Links

| Resource | URL |
|----------|-----|
| GitHub Repository | https://github.com/KaladiSanthoshKumarReddy/capstone |
| Jira Epic | https://jiraeu.epam.com/browse/EPMCDMETST-55183 |
| Confluence Home | https://kb.epam.com/pages/viewpage.action?pageId=2889552361 |
| Architecture Doc | https://kb.epam.com/pages/viewpage.action?pageId=2889554110 |
| HLD | https://kb.epam.com/pages/viewpage.action?pageId=2889554152 |
| FRD | https://kb.epam.com/pages/viewpage.action?pageId=2889556181 |
| API Reference | https://kb.epam.com/pages/viewpage.action?pageId=2889556182 |
| Test Execution Report | https://kb.epam.com/pages/viewpage.action?pageId=2889556184 |
| Deployment Guide | https://kb.epam.com/pages/viewpage.action?pageId=2889556185 |

---

## Tech Stack

| Layer | Technology |
|-------|-----------|
| Frontend | React 18 + TypeScript + Vite + Tailwind CSS |
| State | Zustand (auth), React Router v6 (URL-synced filters) |
| Backend | Node.js + Express + TypeScript |
| Database | SQLite via `@libsql/client` (WASM — no native build tools needed) |
| Auth | JWT (8 h expiry) + SHA-256 password hash |
| Validation | Zod (backend), HTML5 + React (frontend) |
| Testing | Playwright TypeScript (E2E) |
| CI | GitHub Actions |

---

## Quick Start

### Prerequisites

```bash
node --version   # 20+
npm --version    # 10+
```

### 1 — Clone and install

```bash
git clone https://github.com/KaladiSanthoshKumarReddy/capstone.git
cd capstone
npm run install:all
```

### 2 — Configure environment

```bash
cp .env.example .env
# Fill in JIRA_API_TOKEN, CONFLUENCE_API_TOKEN, JWT_SECRET, GITHUB_TOKEN
```

Key variables:

| Variable | Default | Description |
|----------|---------|-------------|
| `BACKEND_PORT` | `4000` | Express server port |
| `FRONTEND_PORT` | `3000` | Vite dev server port |
| `DATABASE_PATH` | `./data/capstone.db` | SQLite file path |
| `JWT_SECRET` | `dev-secret` | Token signing secret — **change in production** |
| `JIRA_BASE_URL` | `https://jiraeu.epam.com` | Jira instance URL |
| `JIRA_API_TOKEN` | — | EPAM Jira Personal Access Token |
| `CONFLUENCE_BASE_URL` | `https://kb.epam.com` | Confluence instance URL |
| `CONFLUENCE_API_TOKEN` | — | EPAM Confluence Personal Access Token |
| `GITHUB_TOKEN` | — | GitHub PAT with `repo` scope |

### 3 — Run in development

```bash
npm run dev
# Backend  → http://localhost:4000
# Frontend → http://localhost:3000
```

### 4 — Build for production

```bash
npm run build
# Backend  → backend/dist/
# Frontend → frontend/dist/
```

Start production server:

```bash
cd backend && node dist/index.js
cd frontend && npx vite preview  # → http://localhost:4173
```

---

## Project Structure

```
capstone/
├── backend/
│   ├── src/
│   │   ├── db/init.ts             # SQLite schema + singleton client (@libsql/client)
│   │   ├── middleware/auth.ts     # JWT verify middleware
│   │   └── routes/
│   │       ├── auth.ts            # POST /api/auth/login|register
│   │       ├── items.ts           # GET|POST|PATCH|DELETE /api/items
│   │       └── debug.ts           # Dev-only debug utilities (excluded from prod)
│   └── dist/                      # Compiled output (git-ignored)
├── frontend/
│   ├── src/
│   │   ├── api/                   # Axios client + typed items API helpers
│   │   ├── components/
│   │   │   ├── ItemCard.tsx       # Single item: inline edit, status toggle, delete
│   │   │   ├── ItemForm.tsx       # Create new item form
│   │   │   ├── ItemList.tsx       # Items grid + empty state
│   │   │   ├── Navbar.tsx         # App bar with user email + logout
│   │   │   ├── Pagination.tsx     # Prev/Next + page indicator
│   │   │   ├── ProtectedRoute.tsx # Auth guard; redirects to /login if no token
│   │   │   ├── SearchBar.tsx      # Debounced text search (300ms)
│   │   │   └── StatusFilter.tsx   # All / Active / Completed / Archived dropdown
│   │   ├── pages/
│   │   │   ├── Dashboard.tsx      # Main page; owns search/filter/page state + URL sync
│   │   │   ├── Login.tsx          # Sign-in form
│   │   │   ├── Register.tsx       # Account creation form
│   │   │   └── NotFound.tsx       # 404 page
│   │   ├── store/authStore.ts     # Zustand auth state (token + email, localStorage)
│   │   └── types/index.ts         # Shared TypeScript interfaces (Item, PaginationMeta)
│   └── dist/                      # Vite production bundle (git-ignored)
├── tests/
│   ├── e2e/
│   │   ├── helpers/auth.ts        # registerUser + loginViaApi (API-level helpers)
│   │   ├── pages/
│   │   │   ├── LoginPage.ts       # Page Object Model for /login
│   │   │   └── DashboardPage.ts   # Page Object Model for /dashboard
│   │   └── specs/
│   │       ├── login.spec.ts      # 22 tests: UI, validation, auth, route guards
│   │       ├── dashboard.spec.ts  # 25 tests: layout, logout, item interactions
│   │       └── items.spec.ts      # 14 tests: CRUD, search/filter, pagination
│   ├── features/
│   │   └── items.feature          # Gherkin BDD scenarios for item management
│   └── playwright.config.ts       # Chromium + Firefox; auto-starts backend + frontend
├── scripts/
│   ├── push_confluence.py         # Pushes FRD, API Reference, Test Report, Deploy Guide
│   ├── update_home.py             # Updates Confluence Home page navigation table
│   ├── build_arch_doc.py          # Builds Architecture doc payload (already published)
│   ├── build_hld_doc.py           # Builds HLD doc payload (already published)
│   └── init-git.sh                # One-time Git + GitHub remote setup
├── .claude/agents/                # Claude Code agent definitions (BA, Architect, Dev, QA…)
├── docs/SDLC_GUIDE.md             # Phase-by-phase AI prompt guide
├── .github/workflows/ci.yml       # GitHub Actions: build + Playwright on Chromium
├── .env.example                   # Environment variable template
└── package.json                   # Root scripts: install:all, dev, build, test, sdlc
```

---

## API Reference

All endpoints are prefixed `/api`. Authenticated routes require `Authorization: Bearer <token>`.

### Auth

| Method | Endpoint | Auth | Body | Response |
|--------|----------|------|------|----------|
| `POST` | `/auth/register` | — | `{ email, password }` | `201 { success, data: { message } }` |
| `POST` | `/auth/login` | — | `{ email, password }` | `200 { success, data: { token, email } }` |

### Items

| Method | Endpoint | Auth | Query / Body | Response |
|--------|----------|------|--------------|----------|
| `GET` | `/items` | ✅ | `?page&limit&search&status` | `{ success, data: Item[], meta: { total, page, limit, totalPages } }` |
| `POST` | `/items` | ✅ | `{ title, description? }` | `201 { success, data: { id } }` |
| `PATCH` | `/items/:id` | ✅ | `{ title?, description?, status? }` | `{ success, data: Item }` |
| `DELETE` | `/items/:id` | ✅ | — | `200 { success, data: { deleted: true } }` |
| `GET` | `/health` | — | — | `{ success, data: { status: "ok" } }` |

Item status values: `active` | `completed` | `archived`

All responses follow the envelope format: `{ success: boolean, data?: T, error?: string }`

---

## Features

- **JWT Authentication** — register, login, 8-hour tokens, localStorage persistence
- **Protected Routes** — unauthenticated users redirected to `/login`
- **Item CRUD** — create, read, update title/status/description, delete
- **Inline Editing** — click item title to edit in place; Enter saves, Escape cancels
- **Status Toggle** — checkbox flips `active` ↔ `completed` instantly
- **Search** — 300 ms debounced full-text search (title + description)
- **Status Filter** — All / Active / Completed / Archived
- **Pagination** — server-side with `COUNT(*)` + `LIMIT`/`OFFSET`; URL-synced
- **URL State** — `?page=`, `?search=`, `?status=` kept in sync with browser history

---

## Testing

### Run E2E tests

```bash
cd tests
npx playwright test                  # headless, all browsers
npx playwright test --headed         # with browser window
npx playwright test --ui             # Playwright UI mode
npx playwright show-report           # open HTML report
```

### Test coverage

| Spec | Suites | Tests | Coverage Area |
|------|--------|-------|---------------|
| `login.spec.ts` | 4 | 22 | Login UI, validation, authentication, route guards |
| `dashboard.spec.ts` | 4 | 25 | Auth guard, layout, logout, item interactions |
| `items.spec.ts` | 3 | 14 | Item CRUD, search & filter, pagination |
| **Total** | **11** | **61** | |

### CI

GitHub Actions runs on every push to `main`, `develop`, and `feature/**`:
1. Build backend (tsc)
2. Build frontend (tsc + vite)
3. Install Playwright browsers (Chromium)
4. Run E2E tests
5. Upload HTML report as artifact (30-day retention)

---

## Documentation (Confluence)

Scripts under `scripts/` manage the Confluence space. Add `CONFLUENCE_API_TOKEN` to `.env` before running.

```bash
# Push FRD, API Reference, Test Execution Report, Deployment Guide (as child pages)
python scripts/push_confluence.py

# Update the Confluence Home page navigation table
python scripts/update_home.py
```

### Confluence Space Structure

```
Capstone Home                        (pageId: 2889552361)  ✅ updated
├── Architecture Document            (pageId: 2889554110)  ✅ published
├── HLD - High Level Design          (pageId: 2889554152)  ✅ published
├── FRD - Functional Requirements    (pageId: 2889556181)  ✅ updated
├── API Reference - REST API         (pageId: 2889556182)  ✅ updated
├── Test Execution Report (E2E)      (pageId: 2889556184)  ✅ updated
└── Development and Deployment Guide (pageId: 2889556185)  ✅ updated
```

---

## SDLC Phases (AI-Driven)

Each phase uses a dedicated Claude agent inside `.claude/agents/`:

| Phase | Agent | Artifact |
|-------|-------|----------|
| 1 — BA Analysis | `ba-agent` | Jira Epic + 5 Stories |
| 2 — Design | `architect-agent` | Architecture doc + HLD on Confluence |
| 3 — Development | `dev-agent` | Feature commits (stories 55184–55188) |
| 4 — Code Review | `review-agent` | Review findings table |
| 5 — QA | `qa-agent` | 61 Playwright E2E tests |
| 6 — Build/Deploy | — | `npm run build`, local verification |
| 7 — Documentation | `docs-agent` | Confluence FRD + API docs + this README |

Human-in-the-Loop checkpoints occur after each phase before proceeding.

---

## Jira Stories Implemented

| Story | Title | Priority | Status |
|-------|-------|----------|--------|
| [EPMCDMETST-55183](https://jiraeu.epam.com/browse/EPMCDMETST-55183) | [Epic] AI-Driven SDLC Enhancements | — | Open |
| [EPMCDMETST-55184](https://jiraeu.epam.com/browse/EPMCDMETST-55184) | Item Management Dashboard UI | High | Resolved |
| [EPMCDMETST-55185](https://jiraeu.epam.com/browse/EPMCDMETST-55185) | JWT Auth Guard and Protected Routes | High | Resolved |
| [EPMCDMETST-55186](https://jiraeu.epam.com/browse/EPMCDMETST-55186) | Item Search and Status Filter | Medium | Resolved |
| [EPMCDMETST-55187](https://jiraeu.epam.com/browse/EPMCDMETST-55187) | Item Status Update — Complete CRUD | Medium | Resolved |
| [EPMCDMETST-55188](https://jiraeu.epam.com/browse/EPMCDMETST-55188) | Pagination for Items List | Medium | Resolved |

---

## Contributing

```bash
# Create a feature branch
git checkout -b feature/EPMCDMETST-XXXXX-short-desc

# Make changes, then commit with story key
git commit -m "feat(scope): description [EPMCDMETST-XXXXX]"

# Push and open a PR
git push origin feature/EPMCDMETST-XXXXX-short-desc
```

Commit convention: `feat|fix|test|docs|chore(scope): description`

---

**Human Review Required**: README updated. Confluence pages for FRD, API Reference, Test Execution Report, and Deployment Guide are ready to publish — add `CONFLUENCE_API_TOKEN` to `.env` and run `python scripts/push_confluence.py` followed by `python scripts/update_home.py`.
