# AI-driven SDLC — Implementation Plan

Repo: `KaladiSanthoshKumarReddy/capstone`
Branch: `feature/ai-sdlc-plan`

Epic: `EPMCDMETST-55183` — [Capstone] AI-Driven SDLC Enhancements - React Node.js App
Story: `EPMCDMETST-58843` — [Enhancement] Item priority (High/Medium/Low)

Confluence FRD (reference): https://kb.epam.com/spaces/~Santhoshkumarreddy_Kaladi@epam.com/pages/2903965540/FRD+Item+Priority+High+Medium+Low+%E2%80%94+EPMCDMETST-58843

## 1) Scope and deliverables

Goal: Enable a `priority` field on tasks with allowed values `HIGH|MEDIUM|LOW` (canonical in API/DB), defaulting to `MEDIUM`, with full end-to-end support: DB → API → UI → tests & docs.

Deliverables:
- DB column added + idempotent startup migration/backfill.
- Backend API: return `priority` for reads; accept/validate for create/update; default missing to `MEDIUM`.
- Frontend UI: selector in Create/Edit; label + visual badge in list.
- Testing: Playwright E2E create/edit/persist; Vitest unit tests for validation/defaulting.
- Docs: README/API docs updated.

Out of scope: sorting/filtering/bulk updates/notifications/tags.

## 2) Work breakdown structure (WBS) — mapped to Jira

### Epic: EPMCDMETST-55183
- This story delivers a vertical slice: DB → API → UI → Tests → Docs.

### Story: EPMCDMETST-58843 (Item priority)

| Task ID | Area | Description | Outputs |
|---|---|---|---|
| T1 | DB | Add `priority` column to tasks table with default `MEDIUM`; ensure existing rows backfilled | `ALTER TABLE`, init/migration logic |
| T2 | Backend | Add Priority enum + Zod validation, defaulting; update create/update/read endpoints to handle it | Updated routes, schemas, services |
| T3 | Frontend | Add priority selector in Create/Edit; show badge in list; align types and API models | UI components + styling |
| T4 | Tests (Unit) | Vitest tests for validation/defaulting and mapping | `*.test.ts` |
| T5 | Tests (E2E) | Playwright create/edit task with priority; verify persistence after reload | POM + specs |
| T6 | Docs | Update README/API docs describing field, allowed values, defaults, errors | docs updates |
| T7 | CI | Ensure CI runs lint/typecheck/unit/e2e; artifacts on failure | workflow updates if needed |

Acceptance coverage mapping:
- Default = Medium → T1, T2, T3, T4, T5
- Strict validation w/ 400 → T2, T4
- Visible label + badge → T3, T5

## 3) Technical approach

### 3.1 Data model
Canonical values:
- API/DB: `HIGH | MEDIUM | LOW`
- UI labels: `High | Medium | Low`

DB: `tasks.priority TEXT NOT NULL DEFAULT 'MEDIUM'`
- Existing rows should effectively be `MEDIUM`.

### 3.2 Backend changes (Node.js 20 + Express + TypeScript + Zod)

Critical paths to respect:
- `backend/src/db/init.ts` — only add safe, idempotent migration logic.

Expected changes:
- Add enum/schema: `prioritySchema = z.enum(['HIGH','MEDIUM','LOW'])`.
- Create task schema: `priority: prioritySchema.optional().default('MEDIUM')`.
- Update task schema: `priority: prioritySchema.optional()`.
- Ensure all read endpoints include `priority` in response payload.

Error handling:
- Invalid priority must return HTTP 400 with `{ success:false, error: "priority must be one of HIGH, MEDIUM, LOW" }` (or equivalent actionable message).

API notes:
- Base URL: `http://localhost:4000/api`
- Auth header: `Authorization: Bearer <jwt>`
- Response envelope: `{ success: boolean, data?: T, error?: string }`

### 3.3 DB migration strategy (SQLite + better-sqlite3)
Idempotent startup migration:
1. `PRAGMA table_info(tasks)` → if `priority` missing:
   - `ALTER TABLE tasks ADD COLUMN priority TEXT NOT NULL DEFAULT 'MEDIUM'`
2. Defensive backfill:
   - `UPDATE tasks SET priority='MEDIUM' WHERE priority IS NULL`

### 3.4 Frontend changes (React 18 + TS + Vite)
UI requirements:
- Create Task: add a select; default selected `MEDIUM`.
- Edit Task: preselect current value.
- Task list: show label + colored badge.

Suggested test ids:
- `data-testid="task-priority-select"`
- `data-testid="task-priority-badge"`

Suggested badge colors:
- HIGH: red
- MEDIUM: amber/yellow
- LOW: gray/blue

## 4) Test plan

### 4.1 Gherkin scenarios
```gherkin
Feature: Task priority

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

### 4.2 Playwright E2E (TypeScript, POM)
- Extend task Create/Edit POM:
  - `selectPriority('HIGH'|'MEDIUM'|'LOW')`
  - assert badge label/text.
- Specs:
  1) Create (default) → Medium
  2) Create (High) → High
  3) Edit Low→High + reload → High persists

### 4.3 Vitest unit tests
Backend:
- Create schema defaults to `MEDIUM`.
- Invalid priority produces 400 mapping.
- Insert/update mapping persists correct canonical values.

## 5) Build/Deploy/Runbook impact

Local dev:
- Backend startup auto-applies schema change; no manual migration.

Deploy:
- Startup migration must be idempotent for persisted SQLite volumes.

## 6) Risks and mitigations

| Risk | Impact | Mitigation |
|---|---|---|
| Startup migration fails if column already exists | App won’t start | `PRAGMA table_info` check before ALTER |
| UI uses labels instead of canonical values | Validation failures | Use canonical values in `<option value>`; map only for display |
| Existing tests break due to new required field | CI red | DB default + backend default keeps backward compatibility |

## 7) CI strategy (GitHub Actions)
- Required PR checks:
  1) lint + typecheck
  2) unit-tests (Vitest)
  3) e2e-tests (Playwright)
- E2E job:
  - build
  - start backend + frontend
  - run Playwright headless
  - upload Playwright report artifact on failure

## 8) Implementation sequence
1. T1 DB migration
2. T2 Backend API + validation
3. T3 Frontend UI
4. T4 Unit tests
5. T5 E2E tests
6. T6 Docs
7. T7 CI hardening

## 9) Definition of Done
- AC met per FRD
- Unit + E2E passing in CI
- Docs updated
