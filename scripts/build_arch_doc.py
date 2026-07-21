import json, os

OUTDIR = os.environ.get('TEMP', '/tmp') + '/jira_stories'
os.makedirs(OUTDIR, exist_ok=True)

content = """<h1>Architecture Document</h1>
<p><strong>Project:</strong> Capstone &mdash; AI-Driven SDLC &nbsp;|&nbsp;
<strong>Author:</strong> Santhoshkumarreddy Kaladi &nbsp;|&nbsp;
<strong>Group:</strong> mm-learning-group-1</p>
<p><strong>Jira Epic:</strong> <a href="https://jiraeu.epam.com/browse/EPMCDMETST-55183">EPMCDMETST-55183</a></p>

<hr/>
<h2>1. System Overview</h2>
<p>This capstone builds an AI-assisted SDLC pipeline on a brownfield React + Node.js application.
Each SDLC phase (Analysis, Design, Development, QA, Review, Deployment, Documentation) is
powered by a dedicated Claude Code AI agent with Human-in-the-Loop checkpoints.</p>
<p>The application is a task/item management web app demonstrating full-stack development with modern tooling.</p>

<hr/>
<h2>2. Tech Stack</h2>
<table>
<tbody>
<tr><th>Layer</th><th>Technology</th><th>Version</th><th>Justification</th></tr>
<tr><td>Frontend</td><td>React + TypeScript</td><td>18 / 5.x</td><td>Industry-standard SPA with strong typing</td></tr>
<tr><td>Build Tool</td><td>Vite</td><td>5.x</td><td>Fast HMR, native ESM, minimal config</td></tr>
<tr><td>State</td><td>Zustand</td><td>4.x</td><td>Lightweight, no boilerplate, TypeScript-first</td></tr>
<tr><td>Styling</td><td>Tailwind CSS</td><td>3.x</td><td>Utility-first, consistent design</td></tr>
<tr><td>HTTP</td><td>Axios</td><td>1.x</td><td>Interceptors for auth token injection</td></tr>
<tr><td>Routing</td><td>React Router v6</td><td>6.x</td><td>Declarative nested + protected routes</td></tr>
<tr><td>Backend</td><td>Node.js + Express</td><td>22 / 4.x</td><td>Minimal REST API, TypeScript support</td></tr>
<tr><td>Database</td><td>SQLite via libsql</td><td>0.14.x</td><td>Zero-config, file-based, no build tools needed</td></tr>
<tr><td>Auth</td><td>JWT (jsonwebtoken)</td><td>9.x</td><td>Stateless, no session store required</td></tr>
<tr><td>Validation</td><td>Zod</td><td>3.x</td><td>Runtime + compile-time schema validation</td></tr>
<tr><td>E2E Testing</td><td>Playwright TypeScript</td><td>1.45.x</td><td>Cross-browser, Page Object Model</td></tr>
<tr><td>CI/CD</td><td>GitHub Actions</td><td>-</td><td>Auto build + test on every push</td></tr>
</tbody>
</table>

<hr/>
<h2>3. Component Architecture</h2>
<h3>3.1 System Layers</h3>
<ac:structured-macro ac:name="code">
<ac:parameter ac:name="language">text</ac:parameter>
<ac:plain-text-body><![CDATA[
Browser
  |
  +-- React SPA (Vite, port 3001)
        |-- /login          LoginPage.tsx
        |-- /dashboard      ProtectedRoute --> Dashboard.tsx
        |-- authStore.ts    Zustand (JWT state + localStorage)
        |-- axios           proxy --> /api/*
        |
        v
Express API (Node.js, port 4000)
        |-- /api/health
        |-- /api/auth/register   (public)
        |-- /api/auth/login      (public) --> issues JWT
        |-- /api/items           (auth middleware) --> CRUD
        |
        v
SQLite (file: data/capstone.db)
        |-- users  (id, email, password_hash, created_at)
        |-- items  (id, title, description, status, user_id, created_at, updated_at)
]]></ac:plain-text-body>
</ac:structured-macro>

<h3>3.2 Frontend Component Tree</h3>
<ac:structured-macro ac:name="code">
<ac:parameter ac:name="language">text</ac:parameter>
<ac:plain-text-body><![CDATA[
App.tsx
  BrowserRouter
    Routes
      /login       --> LoginPage
      /dashboard   --> ProtectedRoute
                         |-- Navbar (logout button)
                         |-- SearchBar + StatusFilter
                         |-- ItemForm  (add new item)
                         |-- ItemList
                         |     |-- ItemCard x N  (edit, delete, status toggle)
                         |-- Pagination
      *            --> NotFound
]]></ac:plain-text-body>
</ac:structured-macro>

<hr/>
<h2>4. Sequence Diagrams</h2>
<h3>4.1 Login Flow</h3>
<ac:structured-macro ac:name="code">
<ac:parameter ac:name="language">text</ac:parameter>
<ac:plain-text-body><![CDATA[
User       --> LoginPage      : enter email + password
LoginPage  --> Axios          : POST /api/auth/login
Axios      --> Express        : HTTP POST { email, password }
Express    --> SQLite         : SELECT * FROM users WHERE email=?
SQLite     --> Express        : user row
Express    --> Express        : compare SHA-256(password) == password_hash
Express    --> Axios          : 200 { token, email }
Axios      --> authStore      : setToken(token)
authStore  --> localStorage   : persist token
LoginPage  --> Router         : navigate('/dashboard')
]]></ac:plain-text-body>
</ac:structured-macro>

<h3>4.2 Protected Route + Item Load</h3>
<ac:structured-macro ac:name="code">
<ac:parameter ac:name="language">text</ac:parameter>
<ac:plain-text-body><![CDATA[
User          --> Router         : navigate /dashboard
Router        --> ProtectedRoute : render
ProtectedRoute--> authStore      : getToken()
  [no token]  --> Router         : redirect /login
  [token ok]  --> Dashboard      : render
Dashboard     --> Axios          : GET /api/items?page=1&limit=10
Axios         --> Express        : Authorization: Bearer <token>
Express       --> AuthMiddleware : jwt.verify(token)
  [invalid]   --> 401
  [valid]     --> ItemsController
ItemsController --> SQLite       : SELECT ... LIMIT 10 OFFSET 0
SQLite        --> Express        : rows + total
Express       --> Dashboard      : 200 { data: items[], meta: { total, page } }
Dashboard     --> ItemList       : render items
]]></ac:plain-text-body>
</ac:structured-macro>

<hr/>
<h2>5. Data Model</h2>
<ac:structured-macro ac:name="code">
<ac:parameter ac:name="language">sql</ac:parameter>
<ac:plain-text-body><![CDATA[
CREATE TABLE users (
  id            INTEGER PRIMARY KEY AUTOINCREMENT,
  email         TEXT UNIQUE NOT NULL,
  password_hash TEXT NOT NULL,
  created_at    DATETIME DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE items (
  id          INTEGER PRIMARY KEY AUTOINCREMENT,
  title       TEXT NOT NULL,
  description TEXT,
  status      TEXT DEFAULT 'active',   -- active | completed | archived
  user_id     INTEGER REFERENCES users(id),
  created_at  DATETIME DEFAULT CURRENT_TIMESTAMP,
  updated_at  DATETIME                 -- populated on PATCH
);
]]></ac:plain-text-body>
</ac:structured-macro>

<hr/>
<h2>6. API Contract</h2>
<table>
<tbody>
<tr><th>Method</th><th>Path</th><th>Auth</th><th>Body / Params</th><th>Response</th></tr>
<tr><td>POST</td><td>/api/auth/register</td><td>None</td><td>{ email, password }</td><td>201 { success, data: { message } }</td></tr>
<tr><td>POST</td><td>/api/auth/login</td><td>None</td><td>{ email, password }</td><td>200 { success, data: { token, email } }</td></tr>
<tr><td>GET</td><td>/api/items</td><td>Bearer JWT</td><td>?page&amp;limit&amp;search&amp;status</td><td>200 { success, data: items[], meta }</td></tr>
<tr><td>POST</td><td>/api/items</td><td>Bearer JWT</td><td>{ title, description? }</td><td>201 { success, data: { id } }</td></tr>
<tr><td>PATCH</td><td>/api/items/:id</td><td>Bearer JWT</td><td>{ title?, description?, status? }</td><td>200 { success, data: item }</td></tr>
<tr><td>DELETE</td><td>/api/items/:id</td><td>Bearer JWT</td><td>-</td><td>200 { success, data: { deleted: true } }</td></tr>
<tr><td>GET</td><td>/api/health</td><td>None</td><td>-</td><td>200 { success, data: { status: ok } }</td></tr>
</tbody>
</table>
<p>All responses follow envelope: <code>{ success: boolean, data?: T, error?: string }</code></p>

<hr/>
<h2>7. Enhancement Plan</h2>
<table>
<tbody>
<tr><th>Priority</th><th>Story</th><th>Summary</th><th>Components Affected</th></tr>
<tr><td><strong>HIGH</strong></td><td><a href="https://jiraeu.epam.com/browse/EPMCDMETST-55184">EPMCDMETST-55184</a></td><td>Item Management Dashboard UI</td><td>Dashboard.tsx, ItemList.tsx, ItemForm.tsx</td></tr>
<tr><td><strong>HIGH</strong></td><td><a href="https://jiraeu.epam.com/browse/EPMCDMETST-55185">EPMCDMETST-55185</a></td><td>JWT Auth Guard + Protected Routes</td><td>authStore.ts, ProtectedRoute.tsx, middleware/auth.ts</td></tr>
<tr><td>MED</td><td><a href="https://jiraeu.epam.com/browse/EPMCDMETST-55186">EPMCDMETST-55186</a></td><td>Item Search and Status Filter</td><td>SearchBar.tsx, GET /api/items query params</td></tr>
<tr><td>MED</td><td><a href="https://jiraeu.epam.com/browse/EPMCDMETST-55187">EPMCDMETST-55187</a></td><td>Item Status Update - CRUD Complete</td><td>ItemCard.tsx, PATCH /api/items/:id</td></tr>
<tr><td>MED</td><td><a href="https://jiraeu.epam.com/browse/EPMCDMETST-55188">EPMCDMETST-55188</a></td><td>Pagination for Items List</td><td>Pagination.tsx, SQL LIMIT/OFFSET</td></tr>
</tbody>
</table>

<hr/>
<h2>8. Non-Functional Requirements</h2>
<table>
<tbody>
<tr><th>Category</th><th>Requirement</th></tr>
<tr><td>Performance</td><td>API responses under 200ms for CRUD operations on SQLite</td></tr>
<tr><td>Security</td><td>JWT expiry 8h; passwords SHA-256 hashed; no secrets in source code</td></tr>
<tr><td>Testability</td><td>All UI elements carry data-testid; Playwright covers happy path + error paths</td></tr>
<tr><td>Maintainability</td><td>TypeScript strict mode; controller/service/repository layer separation</td></tr>
<tr><td>Deployment</td><td>Local: npm run dev; CI: GitHub Actions builds + Playwright on Chromium</td></tr>
</tbody>
</table>"""

payload = {
    "type": "page",
    "title": "Architecture Document - React Node.js Capstone",
    "ancestors": [{"id": "2889552361"}],
    "space": {"key": "~Santhoshkumarreddy_Kaladi@epam.com"},
    "body": {
        "storage": {
            "value": content,
            "representation": "storage"
        }
    }
}

path = OUTDIR + "/arch_doc.json"
with open(path, "w", encoding="utf-8") as f:
    json.dump(payload, f, ensure_ascii=False)
print("Written:", path)
