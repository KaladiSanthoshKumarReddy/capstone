import { Router, Request, Response } from 'express'
import { getDb } from '../db/init'

const router = Router()

router.get('/', (_req: Request, res: Response) => {
  res.type('html').send(`<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1" />
  <title>Capstone Debug Tables</title>
  <style>
    :root {
      --bg: #f6f7fb;
      --card: #ffffff;
      --text: #18202a;
      --muted: #5f6b7a;
      --line: #d9e0ea;
      --head: #eef3fa;
      --accent: #1f6feb;
      --ok: #0f7b6c;
    }
    * { box-sizing: border-box; }
    body {
      margin: 0;
      background: radial-gradient(circle at top right, #e3eeff 0%, var(--bg) 38%);
      color: var(--text);
      font-family: "Segoe UI", Tahoma, Geneva, Verdana, sans-serif;
      line-height: 1.45;
    }
    .wrap {
      max-width: 1200px;
      margin: 24px auto;
      padding: 0 16px 24px;
    }
    .head {
      background: var(--card);
      border: 1px solid var(--line);
      border-radius: 14px;
      padding: 14px 16px;
      margin-bottom: 14px;
      display: flex;
      align-items: center;
      justify-content: space-between;
      gap: 12px;
      flex-wrap: wrap;
    }
    .title {
      margin: 0;
      font-size: 20px;
      font-weight: 700;
    }
    .meta {
      color: var(--muted);
      font-size: 13px;
    }
    .btn {
      border: 1px solid #b9c7de;
      background: #f8fbff;
      color: #0f3875;
      border-radius: 8px;
      padding: 8px 12px;
      cursor: pointer;
      font-size: 13px;
      font-weight: 600;
    }
    .grid {
      display: grid;
      gap: 14px;
      grid-template-columns: 1fr;
    }
    @media (min-width: 960px) {
      .grid { grid-template-columns: 1fr 1fr; }
    }
    .card {
      background: var(--card);
      border: 1px solid var(--line);
      border-radius: 14px;
      overflow: hidden;
      min-width: 0;
    }
    .card h2 {
      margin: 0;
      padding: 12px 14px;
      font-size: 16px;
      background: linear-gradient(180deg, #f9fbff 0%, #f2f6fc 100%);
      border-bottom: 1px solid var(--line);
    }
    .count {
      color: var(--ok);
      font-size: 12px;
      margin-left: 8px;
      font-weight: 700;
    }
    .table-wrap {
      overflow: auto;
      max-height: 62vh;
    }
    table {
      width: 100%;
      border-collapse: collapse;
      font-size: 13px;
    }
    th, td {
      border-bottom: 1px solid var(--line);
      padding: 8px 10px;
      text-align: left;
      white-space: nowrap;
      vertical-align: top;
    }
    th {
      position: sticky;
      top: 0;
      z-index: 1;
      background: var(--head);
      font-weight: 700;
    }
    td.desc {
      min-width: 180px;
      max-width: 340px;
      white-space: normal;
      color: #2f3b4d;
    }
    .empty {
      padding: 16px;
      color: var(--muted);
      font-size: 13px;
    }
    .err {
      color: #9c2a2a;
      font-weight: 600;
      padding: 12px 14px;
    }
    .pill {
      display: inline-block;
      border-radius: 999px;
      padding: 2px 8px;
      font-size: 11px;
      border: 1px solid #bdd0f3;
      background: #edf3ff;
      color: #1b4f98;
    }
  </style>
</head>
<body>
  <div class="wrap">
    <div class="head">
      <div>
        <h1 class="title">Capstone Local Debug Tables</h1>
        <div class="meta">Read-only local inspector for users and items on port 4000.</div>
      </div>
      <button id="refresh" class="btn" type="button">Refresh</button>
    </div>

    <div id="error" class="err" style="display:none;"></div>

    <div class="grid">
      <section class="card">
        <h2>Users <span id="usersCount" class="count"></span></h2>
        <div id="usersWrap" class="table-wrap"></div>
      </section>

      <section class="card">
        <h2>Items <span id="itemsCount" class="count"></span></h2>
        <div id="itemsWrap" class="table-wrap"></div>
      </section>
    </div>
  </div>

  <script>
    const usersWrap = document.getElementById('usersWrap');
    const itemsWrap = document.getElementById('itemsWrap');
    const usersCount = document.getElementById('usersCount');
    const itemsCount = document.getElementById('itemsCount');
    const errorEl = document.getElementById('error');
    const refreshBtn = document.getElementById('refresh');

    function esc(value) {
      return String(value ?? '')
        .replaceAll('&', '&amp;')
        .replaceAll('<', '&lt;')
        .replaceAll('>', '&gt;')
        .replaceAll('"', '&quot;')
        .replaceAll("'", '&#39;');
    }

    function renderUsers(rows) {
      usersCount.textContent = rows.length + ' row(s)';
      if (!rows.length) {
        usersWrap.innerHTML = '<div class="empty">No users found.</div>';
        return;
      }
      const body = rows.map(function (r) {
        return '<tr>'
          + '<td>' + esc(r.id) + '</td>'
          + '<td>' + esc(r.email) + '</td>'
          + '<td>' + esc(r.created_at) + '</td>'
          + '</tr>';
      }).join('');
      usersWrap.innerHTML = '<table>'
        + '<thead><tr><th>ID</th><th>Email</th><th>Created At</th></tr></thead>'
        + '<tbody>' + body + '</tbody>'
        + '</table>';
    }

    function renderItems(rows) {
      itemsCount.textContent = rows.length + ' row(s)';
      if (!rows.length) {
        itemsWrap.innerHTML = '<div class="empty">No items found.</div>';
        return;
      }
      const body = rows.map(function (r) {
        return '<tr>'
          + '<td>' + esc(r.id) + '</td>'
          + '<td>' + esc(r.title) + '</td>'
          + '<td class="desc">' + esc(r.description) + '</td>'
          + '<td><span class="pill">' + esc(r.status) + '</span></td>'
          + '<td>' + esc(r.user_id) + '</td>'
          + '<td>' + esc(r.created_at) + '</td>'
          + '<td>' + esc(r.updated_at) + '</td>'
          + '</tr>';
      }).join('');
      itemsWrap.innerHTML = '<table>'
        + '<thead><tr>'
        + '<th>ID</th><th>Title</th><th>Description</th><th>Status</th>'
        + '<th>User ID</th><th>Created At</th><th>Updated At</th>'
        + '</tr></thead>'
        + '<tbody>' + body + '</tbody>'
        + '</table>';
    }

    async function loadData() {
      errorEl.style.display = 'none';
      try {
        const [usersRes, itemsRes] = await Promise.all([
          fetch('/api/debug/users'),
          fetch('/api/debug/items')
        ]);

        if (!usersRes.ok || !itemsRes.ok) {
          throw new Error('Failed to load debug data.');
        }

        const users = await usersRes.json();
        const items = await itemsRes.json();
        renderUsers(users.data || []);
        renderItems(items.data || []);
      } catch (err) {
        errorEl.textContent = err instanceof Error ? err.message : 'Unknown error';
        errorEl.style.display = 'block';
      }
    }

    refreshBtn.addEventListener('click', loadData);
    loadData();
  </script>
</body>
</html>`)
})

// Local debug endpoint: list users without exposing password hashes.
router.get('/users', async (_req: Request, res: Response) => {
  const db = getDb()
  const result = await db.execute({
    sql: 'SELECT id, email, created_at FROM users ORDER BY created_at DESC',
    args: [],
  })
  return res.json({ success: true, data: result.rows })
})

// Local debug endpoint: list items from newest to oldest.
router.get('/items', async (_req: Request, res: Response) => {
  const db = getDb()
  const result = await db.execute({
    sql: 'SELECT id, title, description, status, user_id, created_at, updated_at FROM items ORDER BY created_at DESC',
    args: [],
  })
  return res.json({ success: true, data: result.rows })
})

export default router