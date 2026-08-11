# AI-driven SDLC — Implementation Plan (capstone)

Repo: `KaladiSanthoshKumarReddy/capstone`
Branch: `feature/ai-sdlc-plan`
File: `docs/ai/ai-sdlc-plan.md`

Confluence FRD (reference):
https://kb.epam.com/spaces/~Santhoshkumarreddy_Kaladi@epam.com/pages/2903958180/FRD+-+Capstone+Enhancements+EPMCDMETST-55183

---

## 1) Scope statement (In / Out)

### In scope (this run)
**Feature: Item Priority (HIGH / MEDIUM / LOW)**
- Add a `priority` attribute to task items with allowed values: `HIGH | MEDIUM | LOW`
- Default priority for new items: `MEDIUM`
- Backend validation rejects invalid priority values
- UI: user can set priority on create/edit; priority displayed in list as badge/label
- Automated tests: default + create/edit (Playwright + unit/validation)

### Out of scope (explicitly not in this run)
- Due dates, reminders, email notifications
- Tags/categories
- Bulk operations
- Audit/history log
- Dark mode/theme
- **CSV export** is a separate story in the Epic (EPMCDMETST-58844) and is **not implemented** in this run

---

## 2) Jira mapping / Traceability

Epic:
- **EPMCDMETST-55183** — [Capstone] AI-Driven SDLC Enhancements - React Node.js App

Priority feature scope (implement + test):
- **Story:** EPMCDMETST-58843 — [Enhancement] Item priority (High/Medium/Low)
- **Tasks:**
  - EPMCDMETST-58866 — Implement backend support for item priority field
  - EPMCDMETST-58867 — Implement frontend UI for setting and displaying item priority
  - EPMCDMETST-58868 — Add automated tests for item priority (E2E + validation)
  - EPMCDMETST-58949 — Add item priority column + API validation (default MEDIUM)
  - EPMCDMETST-58950 — Add priority selector + badge to item create/edit UI
  - EPMCDMETST-58951 — Add Playwright tests for item priority (create/edit/default)

Related, explicitly out-of-scope this run:
- **Story:** EPMCDMETST-58844 — Export items to CSV

---

## 3) Architecture constraints & conventions (brownfield)

**Do not redesign** these critical paths:
- `backend/src/middleware/auth.ts` — JWT auth guard
- `backend/src/db/init.ts` — SQLite initialization (only add safe, idempotent migration)
- `frontend/src/store/authStore.ts` — Zustand auth state
- `frontend/src/api/client.ts` — Axios client with token injection

API conventions:
- Base URL: `http://localhost:4000/api`
- Auth header: `Authorization: Bearer <jwt>`
- Response envelope: `{ success: boolean, data?: T, error?: string }`

---

## 4) Backend / DB plan

### 4.1 DB schema change (SQLite)
Target change (conceptual):
- Add `priority` column to the tasks/items table
- Type: `TEXT NOT NULL`
- Default: `'MEDIUM'`

Idempotent startup migration strategy (in `backend/src/db/init.ts`):
1. Inspect table schema with `PRAGMA table_info(<table>)`
2. If `priority` column is missing:
   - `ALTER TABLE <table> ADD COLUMN priority TEXT NOT NULL DEFAULT 'MEDIUM'`
3. Defensive backfill:
   - `UPDATE <table> SET priority='MEDIUM' WHERE priority IS NULL OR priority=''`

### 4.2 Backend validation & behavior
Add canonical enum:
- `HIGH | MEDIUM | LOW`

Zod schemas (intent):
- `prioritySchema = z.enum(['HIGH','MEDIUM','LOW'])`
- Create: `priority` optional with `.default('MEDIUM')`
- Update: `priority` optional (no default)

Endpoint behavior:
- All read responses include `priority`
- Create:
  - if client omits `priority`, API stores `MEDIUM`
  - if client sends invalid `priority`, API returns **400** with `{ success:false, error }`
- Update:
  - if client sends valid `priority`, persists new value

---

## 5) Frontend plan

### 5.1 Types & models
- Extend the task/item type to include:
  - `priority: 'HIGH' | 'MEDIUM' | 'LOW'`

### 5.2 UI changes
Create/Edit form:
- Add a priority selector (select or radio group)
- Default selection: `MEDIUM` on create
- Edit: pre-select persisted value

List view:
- Display `priority` as a badge/label
- Suggested mapping (display only):
  - HIGH → “High”
  - MEDIUM → “Medium”
  - LOW → “Low”

**Required `data-testid` attributes** (for stable E2E):
- `data-testid="task-priority-select"`
- `data-testid="task-priority-badge"`

---

## 6) Test plan

### 6.1 Gherkin scenarios (acceptance)
```gherkin
Feature: Item priority

  Scenario: Create a task with default priority
    Given I am logged in
    When I create a task without selecting a priority
    Then the task is created successfully
    And the task shows priority "Medium"

  Scenario: Create a task with High priority
    Given I am logged in
    When I create a task with priority "High"
    Then the task shows priority "High" in the list

  Scenario: Edit a task priority
    Given I am logged in
    And a task exists with priority "Low"
    When I edit the task and set priority to "High"
    Then the task shows priority "High" after saving
    And the priority persists after page reload

  Scenario: Invalid priority rejected by API
    Given I am logged in
    When I call create task API with priority "URGENT"
    Then the API responds with status 400
    And the error message mentions allowed values
```

### 6.2 Playwright E2E (TypeScript, POM)
Planned specs:
1. Create task without touching priority → badge shows Medium
2. Create task with HIGH → badge shows High
3. Edit task LOW → HIGH and reload → HIGH persists

Planned POM additions:
- `selectPriority('HIGH'|'MEDIUM'|'LOW')`
- `expectPriorityBadge('High'|'Medium'|'Low')`

### 6.3 Vitest unit tests
Backend unit test points:
- Create schema defaults to `MEDIUM` when priority omitted
- Invalid `priority` yields 400 and correct error envelope
- Update persists valid enum values

---

## 7) Build plan & local deploy plan

Build (typical):
- `pnpm install`
- `pnpm -C backend build`
- `pnpm -C frontend build`

Local run (typical):
- `pnpm -C backend dev`
- `pnpm -C frontend dev`

Expectation:
- On backend startup, schema migration runs safely and idempotently.

---

## 8) CI strategy (GitHub Actions)

PR gates:
- Lint + typecheck
- Unit tests (Vitest)
- E2E tests (Playwright)

E2E job outline:
- install deps
- build
- start backend + frontend
- run Playwright headless
- upload Playwright report artifacts on failure

---

## 9) Risks / mitigations

| Risk | Impact | Mitigation |
|---|---|---|
| SQLite migration fails or re-runs | App won’t boot / flaky CI | Check column existence via `PRAGMA table_info` before `ALTER TABLE` |
| UI uses labels instead of canonical enum values | 400 validation failures | Use canonical values in `<option value>`; map to labels for display only |
| E2E selectors become brittle | Flaky tests | Use `data-testid` attributes consistently |

---

## 10) Milestones

1. DB migration + backfill complete
2. Backend: schemas + endpoints updated, validation in place
3. Frontend: selector + list badge complete
4. Tests: unit + E2E green
5. Docs updated

