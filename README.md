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

| Variable | Description |
|----------|-------------|
| `BACKEND_PORT` | Express port (default `4000`) |
| `FRONTEND_PORT` | Vite dev port (default `3000`) |
| `DATABASE_PATH` | SQLite file path (default `./data/capstone.db`) |
| `JWT_SECRET` | Token signing secret — **change in production** |
| `JIRA_API_TOKEN` | EPAM Jira Personal Access Token |
| `CONFLUENCE_API_TOKEN` | EPAM Confluence Personal Access Token |
| `GITHUB_TOKEN` | GitHub PAT with `repo` scope |

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
cd frontend && npx vite preview
```

---

## Project Structure

```
capstone/
├── backend/
│   ├── src/
│   │   ├── db/init.ts          # SQLite schema + singleton client
│   │   ├── middleware/auth.ts  # JWT verify middleware
│   │   └── routes/
│   │       ├── auth.ts         # POST /api/auth/login|register
│   │       └── items.ts        # GET|POST|PATCH|DELETE /api/items
│   └── dist/                   # Compiled output (git-ignored)
├── frontend/
│   ├── src/
│   │   ├── api/                # Axios client + items API helpers
│   │   ├── components/         # ItemCard, ItemForm, SearchBar, etc.
│   │   ├── pages/              # Login, Dashboard, NotFound
│   │   ├── store/authStore.ts  # Zustand auth state
│   │   └── types/index.ts      # Shared TypeScript interfaces
│   └── dist/                   # Vite production bundle (git-ignored)
├── tests/
│   ├── e2e/
│   │   ├── helpers/auth.ts     # registerUser, loginViaApi helpers
│   │   ├── pages/              # Page Object Models (Login, Dashboard)
│   │   └── specs/              # login.spec.ts, dashboard.spec.ts, items.spec.ts
│   ├── features/               # Gherkin .feature files
│   └── playwright.config.ts
├── .claude/agents/             # Claude Code agent definitions
├── docs/SDLC_GUIDE.md          # Phase-by-phase AI prompts
├── scripts/                    # Confluence doc build scripts
└── .github/workflows/ci.yml    # GitHub Actions build + test
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
| `DELETE` | `/items/:id` | ✅ | — | `200 { success }` |
| `GET` | `/health` | — | — | `{ success, data: { status: "ok" } }` |

Item status values: `active` | `completed` | `archived`

---

## Features

- **JWT Authentication** — register, login, 8-hour tokens, localStorage persistence
- **Protected Routes** — unauthenticated users redirected to `/login`
- **Item CRUD** — create, read, update title/status/description, delete
- **Inline Editing** — click item title to edit in place; Enter saves, Escape cancels
- **Status Toggle** — checkbox flips active ↔ completed instantly
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

| Spec | Suites | Tests |
|------|--------|-------|
| `login.spec.ts` | UI, Validation, Authentication, Route Guards | 22 |
| `dashboard.spec.ts` | Auth Guard, Layout, Logout, Item Interactions | 25 |
| `items.spec.ts` | Item Management, Search & Filter, Pagination | 14 |
| **Total** | | **61** |

### CI

GitHub Actions runs on every push to `main`:
1. Build backend (tsc)
2. Build frontend (tsc + vite)
3. Install Playwright browsers
4. Run E2E tests on Chromium

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
| EPMCDMETST-55183 | [Epic] AI-Driven SDLC Enhancements | — | Open |
| EPMCDMETST-55184 | Item Management Dashboard UI | High | Resolved |
| EPMCDMETST-55185 | JWT Auth Guard and Protected Routes | High | Resolved |
| EPMCDMETST-55186 | Item Search and Status Filter | Medium | Resolved |
| EPMCDMETST-55187 | Item Status Update — Complete CRUD | Medium | Resolved |
| EPMCDMETST-55188 | Pagination for Items List | Medium | Resolved |

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
