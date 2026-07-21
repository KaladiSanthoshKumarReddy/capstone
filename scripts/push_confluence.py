import json, subprocess, tempfile, os, sys

env_path = os.path.join(os.path.dirname(__file__), '..', '.env')
with open(env_path) as f:
    env_lines = f.read().splitlines()

def get_env(key):
    for line in env_lines:
        if line.startswith(key + '='):
            return line.split('=', 1)[1].strip()
    return None

TOKEN  = get_env('CONFLUENCE_API_TOKEN')
BASE   = 'https://kb.epam.com'
PARENT = '2889552361'
SPACE  = '~Santhoshkumarreddy_Kaladi@epam.com'

pages = [
    {
        "title": "FRD - Functional Requirements Document",
        "body": """<h1>Functional Requirements Document</h1>
<p><strong>Project:</strong> Capstone - AI-Driven SDLC | <strong>Group:</strong> mm-learning-group-1 | <strong>Jira Epic:</strong> EPMCDMETST-55183</p>
<h2>1. Purpose</h2>
<p>This document captures the functional requirements for the brownfield React + Node.js task-management application enhanced through an AI-assisted SDLC pipeline.</p>
<h2>2. Scope</h2>
<p>The application provides authenticated users the ability to manage personal items (tasks) through a web interface. The backend exposes a REST API consumed by the React SPA.</p>
<h2>3. Functional Requirements</h2>
<h3>3.1 Authentication (EPMCDMETST-55185)</h3>
<table><tr><th>ID</th><th>Requirement</th><th>Priority</th></tr>
<tr><td>FR-01</td><td>User shall be able to register with email and password (min 6 chars)</td><td>High</td></tr>
<tr><td>FR-02</td><td>User shall be able to log in with valid credentials and receive a JWT</td><td>High</td></tr>
<tr><td>FR-03</td><td>JWT token shall expire after 8 hours</td><td>High</td></tr>
<tr><td>FR-04</td><td>Unauthenticated users accessing protected routes shall be redirected to /login</td><td>High</td></tr>
<tr><td>FR-05</td><td>User shall be able to log out; token and email cleared from browser storage</td><td>High</td></tr>
<tr><td>FR-06</td><td>Logged-in email shall be visible in the navbar</td><td>Medium</td></tr></table>
<h3>3.2 Item Management Dashboard (EPMCDMETST-55184)</h3>
<table><tr><th>ID</th><th>Requirement</th><th>Priority</th></tr>
<tr><td>FR-07</td><td>Dashboard shall display a list of the authenticated user items</td><td>High</td></tr>
<tr><td>FR-08</td><td>User shall be able to create an item with a title and optional description</td><td>High</td></tr>
<tr><td>FR-09</td><td>User shall be able to delete an item (with confirmation dialog)</td><td>High</td></tr>
<tr><td>FR-10</td><td>User shall be able to inline-edit an item title (click-to-edit, Enter saves, Escape cancels)</td><td>Medium</td></tr>
<tr><td>FR-11</td><td>An empty state message shall appear when no items exist or match filters</td><td>Low</td></tr>
<tr><td>FR-12</td><td>Item count shall be displayed in the dashboard header</td><td>Low</td></tr></table>
<h3>3.3 Search and Status Filter (EPMCDMETST-55186)</h3>
<table><tr><th>ID</th><th>Requirement</th><th>Priority</th></tr>
<tr><td>FR-13</td><td>User shall be able to search items by title or description (debounced 300ms)</td><td>Medium</td></tr>
<tr><td>FR-14</td><td>User shall be able to filter items by status: All / Active / Completed / Archived</td><td>Medium</td></tr>
<tr><td>FR-15</td><td>Search and filter state shall be persisted in the URL query string (?search=, ?status=)</td><td>Medium</td></tr>
<tr><td>FR-16</td><td>Changing search or filter shall reset page to 1</td><td>Low</td></tr></table>
<h3>3.4 Item Status CRUD (EPMCDMETST-55187)</h3>
<table><tr><th>ID</th><th>Requirement</th><th>Priority</th></tr>
<tr><td>FR-17</td><td>Item status values shall be: active (default), completed, archived</td><td>Medium</td></tr>
<tr><td>FR-18</td><td>User shall be able to toggle an item between active and completed via checkbox</td><td>Medium</td></tr>
<tr><td>FR-19</td><td>PATCH /api/items/:id shall support partial update of title, description, status</td><td>Medium</td></tr>
<tr><td>FR-20</td><td>updated_at timestamp shall be set on every PATCH operation</td><td>Low</td></tr></table>
<h3>3.5 Pagination (EPMCDMETST-55188)</h3>
<table><tr><th>ID</th><th>Requirement</th><th>Priority</th></tr>
<tr><td>FR-21</td><td>Items list shall be paginated with 10 items per page</td><td>Medium</td></tr>
<tr><td>FR-22</td><td>Pagination meta (total, page, limit, totalPages) shall be returned in every GET /api/items response</td><td>Medium</td></tr>
<tr><td>FR-23</td><td>Prev/Next controls and X/Y page indicator shall be visible when totalPages &gt; 1</td><td>Medium</td></tr>
<tr><td>FR-24</td><td>Current page shall be persisted in URL (?page=)</td><td>Low</td></tr></table>
<h2>4. Non-Functional Requirements</h2>
<table><tr><th>ID</th><th>Requirement</th></tr>
<tr><td>NFR-01</td><td>API response time &lt; 200ms on local machine for all CRUD operations</td></tr>
<tr><td>NFR-02</td><td>All API endpoints must return envelope: { success, data?, error? }</td></tr>
<tr><td>NFR-03</td><td>TypeScript strict mode - zero compilation errors in both frontend and backend</td></tr>
<tr><td>NFR-04</td><td>No secrets in source code - environment variables only</td></tr>
<tr><td>NFR-05</td><td>Frontend production bundle &lt; 300KB gzipped</td></tr></table>"""
    },
    {
        "title": "API Reference - Capstone REST API",
        "body": """<h1>API Reference - Capstone REST API</h1>
<p><strong>Base URL:</strong> http://localhost:4000/api | <strong>Auth:</strong> Bearer JWT</p>
<p>All responses follow the envelope format: <code>{ &quot;success&quot;: boolean, &quot;data&quot;?: T, &quot;error&quot;?: string }</code></p>
<h2>Authentication</h2>
<h3>POST /auth/register</h3>
<p>Create a new user account.</p>
<table><tr><th>Status</th><th>Description</th></tr>
<tr><td>201</td><td>User created successfully</td></tr>
<tr><td>400</td><td>Invalid input - email format or password &lt; 6 chars</td></tr>
<tr><td>409</td><td>Email already exists</td></tr></table>
<h3>POST /auth/login</h3>
<p>Authenticate and receive a JWT (8h expiry).</p>
<table><tr><th>Status</th><th>Description</th></tr>
<tr><td>200</td><td>Returns { token, email }</td></tr>
<tr><td>400</td><td>Invalid input</td></tr>
<tr><td>401</td><td>Invalid credentials</td></tr></table>
<h2>Items (all require Authorization: Bearer &lt;token&gt;)</h2>
<h3>GET /items</h3>
<p>List items with optional search, status filter, and pagination.</p>
<table><tr><th>Param</th><th>Type</th><th>Default</th><th>Description</th></tr>
<tr><td>page</td><td>number</td><td>1</td><td>Page number</td></tr>
<tr><td>limit</td><td>number</td><td>10</td><td>Items per page (max 100)</td></tr>
<tr><td>search</td><td>string</td><td>-</td><td>Full-text search on title + description</td></tr>
<tr><td>status</td><td>string</td><td>-</td><td>Filter: active | completed | archived</td></tr></table>
<p>Response includes <code>meta: { total, page, limit, totalPages }</code></p>
<h3>POST /items</h3>
<p>Create a new item. Body: <code>{ title: string, description?: string }</code></p>
<p>Returns 201 with <code>{ id }</code> of the created item.</p>
<h3>PATCH /items/:id</h3>
<p>Partially update an item. Body: <code>{ title?, description?, status? }</code></p>
<p>Status values: <strong>active</strong> | <strong>completed</strong> | <strong>archived</strong></p>
<h3>DELETE /items/:id</h3>
<p>Delete an item. Returns 200 <code>{ success: true }</code></p>
<h3>GET /health</h3>
<p>Health check (no auth). Returns <code>{ success: true, data: { status: &quot;ok&quot; } }</code></p>
<h2>Data Model</h2>
<p>Users table: id, email, password_hash, created_at</p>
<p>Items table: id, title, description, status (active/completed/archived), user_id, created_at, updated_at</p>
<h2>Error Codes</h2>
<table><tr><th>Code</th><th>Meaning</th></tr>
<tr><td>400</td><td>Request validation failed (Zod schema error)</td></tr>
<tr><td>401</td><td>Missing, expired, or invalid JWT</td></tr>
<tr><td>409</td><td>Conflict - e.g. email already registered</td></tr>
<tr><td>500</td><td>Unhandled server error</td></tr></table>"""
    },
    {
        "title": "Test Execution Report - E2E Playwright",
        "body": """<h1>Test Execution Report - E2E Playwright</h1>
<p><strong>Date:</strong> 2026-07-21 | <strong>Framework:</strong> Playwright 1.61 + TypeScript | <strong>Branch:</strong> main</p>
<h2>Summary</h2>
<table><tr><th>Spec File</th><th>Suites</th><th>Tests</th><th>Coverage Area</th></tr>
<tr><td>login.spec.ts</td><td>4</td><td>22</td><td>Login UI, validation, authentication, route guards</td></tr>
<tr><td>dashboard.spec.ts</td><td>4</td><td>25</td><td>Auth guard, layout, logout, item interactions</td></tr>
<tr><td>items.spec.ts</td><td>3</td><td>14</td><td>Item CRUD, search and filter, pagination</td></tr>
<tr><td><strong>Total</strong></td><td><strong>11</strong></td><td><strong>61</strong></td><td></td></tr></table>
<h2>Login Feature - 22 Tests</h2>
<table><tr><th>Suite</th><th>Test</th><th>Assertion</th></tr>
<tr><td>UI</td><td>renders Sign In heading</td><td>heading visible</td></tr>
<tr><td>UI</td><td>shows email, password inputs, login button</td><td>all 3 visible</td></tr>
<tr><td>UI</td><td>email input has type=email</td><td>attribute check</td></tr>
<tr><td>UI</td><td>password input has type=password</td><td>attribute check</td></tr>
<tr><td>UI</td><td>inputs have required attribute</td><td>attribute check</td></tr>
<tr><td>UI</td><td>login button label is Login</td><td>text content</td></tr>
<tr><td>UI</td><td>login button enabled on load</td><td>not disabled</td></tr>
<tr><td>UI</td><td>no error visible initially</td><td>not visible</td></tr>
<tr><td>Validation</td><td>blocks submit on empty email</td><td>stays on /login</td></tr>
<tr><td>Validation</td><td>blocks submit on empty password</td><td>stays on /login</td></tr>
<tr><td>Validation</td><td>blocks invalid email format</td><td>stays on /login</td></tr>
<tr><td>Auth</td><td>Invalid credentials for unknown email</td><td>error text</td></tr>
<tr><td>Auth</td><td>Invalid credentials for wrong password</td><td>error text</td></tr>
<tr><td>Auth</td><td>error in red styling</td><td>class contains text-red</td></tr>
<tr><td>Auth</td><td>button disabled + Signing in during submit</td><td>route intercept</td></tr>
<tr><td>Auth</td><td>redirects to /dashboard on success</td><td>URL check</td></tr>
<tr><td>Auth</td><td>token in localStorage after login</td><td>evaluate()</td></tr>
<tr><td>Auth</td><td>email in localStorage after login</td><td>evaluate()</td></tr>
<tr><td>Auth</td><td>error clears on successful retry</td><td>redirect to dashboard</td></tr>
<tr><td>Route Guards</td><td>/dashboard without token redirects to /login</td><td>URL check</td></tr>
<tr><td>Route Guards</td><td>/ without token redirects to /login</td><td>URL check</td></tr>
<tr><td>Route Guards</td><td>404 page for unknown route</td><td>text visible</td></tr></table>
<h2>Dashboard Feature - 25 Tests</h2>
<table><tr><th>Suite</th><th>Test</th></tr>
<tr><td>Auth Guard</td><td>unauthenticated redirects to /login</td></tr>
<tr><td>Auth Guard</td><td>authenticated can access /dashboard</td></tr>
<tr><td>Layout</td><td>My Items heading</td></tr>
<tr><td>Layout</td><td>item count subtitle</td></tr>
<tr><td>Layout</td><td>Capstone App navbar brand</td></tr>
<tr><td>Layout</td><td>logged-in email in navbar</td></tr>
<tr><td>Layout</td><td>Logout button in navbar</td></tr>
<tr><td>Layout</td><td>item title input visible</td></tr>
<tr><td>Layout</td><td>description input visible</td></tr>
<tr><td>Layout</td><td>add button disabled when empty</td></tr>
<tr><td>Layout</td><td>add button enables when title filled</td></tr>
<tr><td>Layout</td><td>search input with placeholder</td></tr>
<tr><td>Layout</td><td>status filter visible</td></tr>
<tr><td>Layout</td><td>filter has 4 options</td></tr>
<tr><td>Layout</td><td>no perpetual loading spinner</td></tr>
<tr><td>Logout</td><td>logout redirects to /login</td></tr>
<tr><td>Logout</td><td>post-logout /dashboard redirects to /login</td></tr>
<tr><td>Logout</td><td>token cleared from localStorage</td></tr>
<tr><td>Logout</td><td>email cleared from localStorage</td></tr>
<tr><td>Interactions</td><td>add item and input cleared</td></tr>
<tr><td>Interactions</td><td>new item has active badge</td></tr>
<tr><td>Interactions</td><td>search syncs to URL</td></tr>
<tr><td>Interactions</td><td>filter syncs to URL</td></tr>
<tr><td>Interactions</td><td>filter resets page to 1</td></tr>
<tr><td>Interactions</td><td>empty state on no-match search</td></tr></table>
<h2>Test Infrastructure</h2>
<table><tr><th>Component</th><th>Details</th></tr>
<tr><td>Auth helper</td><td>registerUser() + loginViaApi() - API-based auth bypasses UI for dashboard tests</td></tr>
<tr><td>Page Objects</td><td>LoginPage, DashboardPage with typed locators and waitForLoad() helper</td></tr>
<tr><td>webServer</td><td>Playwright auto-starts backend (port 4000) + frontend (port 3000) before tests</td></tr>
<tr><td>Browsers</td><td>Chromium + Firefox (CI: Chromium only)</td></tr>
<tr><td>Retries</td><td>0 locally, 2 on CI</td></tr>
<tr><td>Reporters</td><td>HTML report (playwright-report/) + list</td></tr></table>
<h2>Known Limitations</h2>
<ul>
<li>Tests use shared SQLite DB - parallel execution across workers can cause item count assertions to vary</li>
<li>Pagination tests only assert control visibility (need 11+ items to trigger pagination)</li>
<li>Port 3000/3001 conflicts on dev machine cause Vite to auto-select port 3002</li>
</ul>"""
    },
    {
        "title": "Development and Deployment Guide",
        "body": """<h1>Development and Deployment Guide</h1>
<p><strong>Repository:</strong> https://github.com/KaladiSanthoshKumarReddy/capstone | <strong>Branch:</strong> main</p>
<h2>1. Prerequisites</h2>
<table><tr><th>Tool</th><th>Minimum Version</th><th>Purpose</th></tr>
<tr><td>Node.js</td><td>20.x</td><td>Backend + frontend tooling</td></tr>
<tr><td>npm</td><td>10.x</td><td>Package management</td></tr>
<tr><td>Git</td><td>2.x</td><td>Version control</td></tr>
<tr><td>Claude Code CLI</td><td>latest</td><td>AI-driven SDLC agent orchestration</td></tr></table>
<p>No C++ build tools needed - SQLite is provided via @libsql/client (WASM binary).</p>
<h2>2. First-Time Setup</h2>
<p>Clone the repository and install dependencies:</p>
<pre>git clone https://github.com/KaladiSanthoshKumarReddy/capstone.git
cd capstone
cp .env.example .env
npm run install:all</pre>
<h2>3. Environment Variables</h2>
<table><tr><th>Variable</th><th>Required</th><th>Description</th></tr>
<tr><td>JIRA_BASE_URL</td><td>Yes</td><td>https://jiraeu.epam.com</td></tr>
<tr><td>JIRA_EMAIL</td><td>Yes</td><td>EPAM email</td></tr>
<tr><td>JIRA_API_TOKEN</td><td>Yes</td><td>Jira Personal Access Token</td></tr>
<tr><td>JIRA_PROJECT_KEY</td><td>Yes</td><td>EPMCDMETST</td></tr>
<tr><td>CONFLUENCE_BASE_URL</td><td>Yes</td><td>https://kb.epam.com</td></tr>
<tr><td>CONFLUENCE_API_TOKEN</td><td>Yes</td><td>Confluence Personal Access Token</td></tr>
<tr><td>GIT_REPO_URL</td><td>Yes</td><td>https://github.com/KaladiSanthoshKumarReddy/capstone</td></tr>
<tr><td>GITHUB_TOKEN</td><td>Yes</td><td>GitHub PAT with repo scope</td></tr>
<tr><td>JWT_SECRET</td><td>Yes</td><td>Token signing secret</td></tr>
<tr><td>BACKEND_PORT</td><td>No</td><td>Default: 4000</td></tr>
<tr><td>DATABASE_PATH</td><td>No</td><td>Default: ./data/capstone.db</td></tr></table>
<h2>4. Development Workflow</h2>
<p>Start both servers concurrently:</p>
<pre>npm run dev
# Backend  (ts-node-dev)  -&gt; http://localhost:4000
# Frontend (Vite HMR)    -&gt; http://localhost:3000</pre>
<h2>5. Build</h2>
<pre>npm run build
# Compiles backend TypeScript -&gt; backend/dist/
# Bundles frontend Vite     -&gt; frontend/dist/</pre>
<h2>6. Running Production Build Locally</h2>
<pre># Terminal 1 - backend
cd backend &amp;&amp; node dist/index.js

# Terminal 2 - frontend (static preview)
cd frontend &amp;&amp; npx vite preview
# -&gt; http://localhost:4173</pre>
<h2>7. Running Tests</h2>
<pre>cd tests
npx playwright test              # Run all tests headless
npx playwright test --headed     # With browser window
npx playwright test --ui         # Playwright UI mode
npx playwright show-report       # Open HTML report</pre>
<h2>8. Git Workflow</h2>
<p>Commit convention: <code>feat|fix|test|docs|chore(scope): description</code></p>
<p>Always include the Jira story key in commit messages: <code>[EPMCDMETST-XXXXX]</code></p>
<h2>9. CI/CD (GitHub Actions)</h2>
<p>File: <code>.github/workflows/ci.yml</code></p>
<p>Triggers on push to main. Pipeline: build backend, build frontend, install Playwright browsers, run E2E tests on Chromium.</p>
<h2>10. Common Issues</h2>
<table><tr><th>Issue</th><th>Cause</th><th>Fix</th></tr>
<tr><td>Port 3000 in use</td><td>Another process on the machine</td><td>Vite auto-selects next port (3001, 3002). Update FRONTEND_PORT if needed.</td></tr>
<tr><td>Database locked</td><td>Two backend instances running</td><td>Kill the existing backend process</td></tr>
<tr><td>JWT expired</td><td>Token older than 8 hours</td><td>Log out and log back in</td></tr>
<tr><td>Playwright tests fail on CI</td><td>webServer startup timeout</td><td>Increase timeout in playwright.config.ts</td></tr></table>"""
    }
]

for p in pages:
    payload = {
        "type": "page",
        "title": p["title"],
        "ancestors": [{"id": PARENT}],
        "space": {"key": SPACE},
        "body": {
            "storage": {
                "value": p["body"],
                "representation": "storage"
            }
        }
    }
    with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False, encoding='utf-8') as f:
        json.dump(payload, f, ensure_ascii=False)
        fname = f.name

    r = subprocess.run([
        'curl', '-s', '-X', 'POST',
        f'{BASE}/rest/api/content',
        '-H', f'Authorization: Bearer {TOKEN}',
        '-H', 'Content-Type: application/json',
        '--data-binary', f'@{fname}'
    ], capture_output=True, text=True)
    os.unlink(fname)

    try:
        resp = json.loads(r.stdout)
    except Exception:
        resp = {}

    if resp.get('id'):
        print(f"OK [{resp['id']}] {p['title']}")
        print(f"   {BASE}/pages/viewpage.action?pageId={resp['id']}")
    else:
        # Check for title conflict
        if 'titleAlreadyExistsException' in r.stdout or 'already exists' in r.stdout.lower():
            print(f"SKIP (already exists): {p['title']}")
        else:
            print(f"FAIL: {p['title']}")
            print(f"   {r.stdout[:300]}")
