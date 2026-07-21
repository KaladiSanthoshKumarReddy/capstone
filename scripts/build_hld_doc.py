import json, os

OUTDIR = os.environ.get('TEMP', '/tmp') + '/jira_stories'
os.makedirs(OUTDIR, exist_ok=True)

content = """<h1>High-Level Design (HLD)</h1>
<p><strong>Project:</strong> Capstone &mdash; AI-Driven SDLC &nbsp;|&nbsp;
<strong>Ref:</strong> <a href="https://kb.epam.com/pages/viewpage.action?pageId=2889554110">Architecture Document</a></p>

<hr/>
<h2>1. Feature: Item Management Dashboard UI</h2>
<p><strong>Jira:</strong> <a href="https://jiraeu.epam.com/browse/EPMCDMETST-55184">EPMCDMETST-55184</a> | <strong>Priority:</strong> HIGH</p>
<h3>Frontend Design</h3>
<table><tbody>
<tr><th>Component</th><th>Props</th><th>Responsibility</th></tr>
<tr><td>Dashboard.tsx</td><td>-</td><td>Container: fetches items, owns list state</td></tr>
<tr><td>ItemForm.tsx</td><td>onAdd(item)</td><td>Controlled form: title + description inputs, submit</td></tr>
<tr><td>ItemList.tsx</td><td>items[], onDelete, onUpdate</td><td>Maps items to ItemCard; shows empty state</td></tr>
<tr><td>ItemCard.tsx</td><td>item, onDelete, onUpdate</td><td>Displays single item; delete button with confirmation</td></tr>
</tbody></table>
<h3>Backend Design</h3>
<p>No backend changes needed. Existing endpoints: GET /api/items, POST /api/items, DELETE /api/items/:id.</p>
<h3>Wireframe Description</h3>
<ac:structured-macro ac:name="code"><ac:parameter ac:name="language">text</ac:parameter>
<ac:plain-text-body><![CDATA[
+------------------------------------------+
|  Capstone Dashboard          [Logout]    |
+------------------------------------------+
|  Add New Item                            |
|  [ Title input         ] [Description ] |
|  [        Add Item button              ] |
+------------------------------------------+
|  Items (3)                               |
|  +--------------------------------------+|
|  | Buy groceries      [active] [x]      ||
|  | Write report       [active] [x]      ||
|  | Fix login bug      [active] [x]      ||
|  +--------------------------------------+|
|         [< Prev]  Page 1 of 1  [Next >] |
+------------------------------------------+
]]></ac:plain-text-body></ac:structured-macro>

<hr/>
<h2>2. Feature: JWT Auth Guard and Protected Routes</h2>
<p><strong>Jira:</strong> <a href="https://jiraeu.epam.com/browse/EPMCDMETST-55185">EPMCDMETST-55185</a> | <strong>Priority:</strong> HIGH</p>
<h3>Frontend Design</h3>
<table><tbody>
<tr><th>File</th><th>Role</th></tr>
<tr><td>store/authStore.ts</td><td>Zustand store: token, email, setAuth(), logout(). Reads localStorage on init.</td></tr>
<tr><td>components/ProtectedRoute.tsx</td><td>Reads authStore; renders children if token exists, else redirects to /login.</td></tr>
<tr><td>pages/Login.tsx (update)</td><td>On success: call setAuth(token, email) instead of just navigating.</td></tr>
<tr><td>components/Navbar.tsx</td><td>Shows email + Logout button; calls authStore.logout() + navigate('/login').</td></tr>
</tbody></table>
<h3>Backend Design</h3>
<table><tbody>
<tr><th>File</th><th>Role</th></tr>
<tr><td>middleware/auth.ts</td><td>Reads Authorization header; calls jwt.verify(); attaches userId to req; returns 401 on failure.</td></tr>
<tr><td>routes/items.ts (update)</td><td>Apply authMiddleware to all item routes: router.use(authMiddleware).</td></tr>
</tbody></table>

<hr/>
<h2>3. Feature: Item Search and Status Filter</h2>
<p><strong>Jira:</strong> <a href="https://jiraeu.epam.com/browse/EPMCDMETST-55186">EPMCDMETST-55186</a> | <strong>Priority:</strong> MEDIUM</p>
<h3>Frontend Design</h3>
<table><tbody>
<tr><th>Component</th><th>Behaviour</th></tr>
<tr><td>SearchBar.tsx</td><td>Controlled text input; debounced (300ms); calls onSearch(value)</td></tr>
<tr><td>StatusFilter.tsx</td><td>Dropdown: All / Active / Completed / Archived; calls onFilter(status)</td></tr>
<tr><td>Dashboard.tsx (update)</td><td>Holds search + status state; passes as query params to GET /api/items; syncs to URL</td></tr>
</tbody></table>
<h3>Backend Design</h3>
<p>Update GET /api/items:</p>
<ac:structured-macro ac:name="code"><ac:parameter ac:name="language">sql</ac:parameter>
<ac:plain-text-body><![CDATA[
SELECT * FROM items
WHERE (:search IS NULL OR title LIKE '%' || :search || '%' OR description LIKE '%' || :search || '%')
  AND (:status IS NULL OR status = :status)
ORDER BY created_at DESC
LIMIT :limit OFFSET :offset;
]]></ac:plain-text-body></ac:structured-macro>

<hr/>
<h2>4. Feature: Item Status Update (Complete CRUD)</h2>
<p><strong>Jira:</strong> <a href="https://jiraeu.epam.com/browse/EPMCDMETST-55187">EPMCDMETST-55187</a> | <strong>Priority:</strong> MEDIUM</p>
<h3>Frontend Design</h3>
<table><tbody>
<tr><th>Component</th><th>Behaviour</th></tr>
<tr><td>ItemCard.tsx (update)</td><td>Checkbox toggles status active/completed; click on title enters inline edit mode</td></tr>
</tbody></table>
<h3>Backend Design</h3>
<ac:structured-macro ac:name="code"><ac:parameter ac:name="language">text</ac:parameter>
<ac:plain-text-body><![CDATA[
PATCH /api/items/:id
Body: { title?, description?, status? }  (Zod partial schema)
SQL:  UPDATE items SET title=COALESCE(:title,title), status=COALESCE(:status,status),
      updated_at=CURRENT_TIMESTAMP WHERE id=:id
]]></ac:plain-text-body></ac:structured-macro>

<hr/>
<h2>5. Feature: Pagination for Items List</h2>
<p><strong>Jira:</strong> <a href="https://jiraeu.epam.com/browse/EPMCDMETST-55188">EPMCDMETST-55188</a> | <strong>Priority:</strong> MEDIUM</p>
<h3>Frontend Design</h3>
<table><tbody>
<tr><th>Component</th><th>Props</th><th>Behaviour</th></tr>
<tr><td>Pagination.tsx</td><td>page, totalPages, onPageChange</td><td>Renders Prev/Next + page indicator; boundary buttons disabled</td></tr>
<tr><td>Dashboard.tsx (update)</td><td>-</td><td>page state synced to URL (?page=N); passed to GET /api/items</td></tr>
</tbody></table>
<h3>Backend Design</h3>
<ac:structured-macro ac:name="code"><ac:parameter ac:name="language">text</ac:parameter>
<ac:plain-text-body><![CDATA[
GET /api/items?page=1&limit=10
Response:
{
  success: true,
  data: Item[],
  meta: { total: 42, page: 1, limit: 10, totalPages: 5 }
}
SQL: SELECT COUNT(*) as total FROM items WHERE ...
     SELECT * FROM items WHERE ... LIMIT 10 OFFSET 0
]]></ac:plain-text-body></ac:structured-macro>

<hr/>
<h2>6. Implementation Order</h2>
<table><tbody>
<tr><th>Sprint</th><th>Story</th><th>Depends On</th></tr>
<tr><td>1</td><td>EPMCDMETST-55185 (Auth Guard)</td><td>None &mdash; foundation first</td></tr>
<tr><td>1</td><td>EPMCDMETST-55184 (Dashboard UI)</td><td>Auth Guard (protected route needed)</td></tr>
<tr><td>2</td><td>EPMCDMETST-55187 (CRUD complete)</td><td>Dashboard UI</td></tr>
<tr><td>2</td><td>EPMCDMETST-55188 (Pagination)</td><td>Dashboard UI</td></tr>
<tr><td>3</td><td>EPMCDMETST-55186 (Search/Filter)</td><td>Pagination</td></tr>
</tbody></table>"""

payload = {
    "type": "page",
    "title": "High-Level Design (HLD) - Capstone",
    "ancestors": [{"id": "2889552361"}],
    "space": {"key": "~Santhoshkumarreddy_Kaladi@epam.com"},
    "body": {
        "storage": {
            "value": content,
            "representation": "storage"
        }
    }
}

path = OUTDIR + "/hld_doc.json"
with open(path, "w", encoding="utf-8") as f:
    json.dump(payload, f, ensure_ascii=False)
print("Written:", path)
