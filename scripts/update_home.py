import json, subprocess, tempfile, os

env_path = os.path.join(os.path.dirname(__file__), '..', '.env')
with open(env_path) as f:
    env_lines = f.read().splitlines()

def get_env(key):
    for line in env_lines:
        if line.startswith(key + '='):
            return line.split('=', 1)[1].strip()
    return None

TOKEN = get_env('CONFLUENCE_API_TOKEN')
BASE  = 'https://kb.epam.com'
HOME  = '2889552361'

# Get current version of Home page
r = subprocess.run([
    'curl', '-s',
    f'{BASE}/rest/api/content/{HOME}?expand=version',
    '-H', f'Authorization: Bearer {TOKEN}'
], capture_output=True, text=True)

page = json.loads(r.stdout)
version = page['version']['number']
title   = page['title']

body = """<h1>Capstone - AI-Driven SDLC with Human-in-the-Loop</h1>
<p><strong>Group:</strong> mm-learning-group-1 | <strong>Jira Project:</strong> EPMCDMETST | <strong>GitHub:</strong> <a href="https://github.com/KaladiSanthoshKumarReddy/capstone">KaladiSanthoshKumarReddy/capstone</a></p>
<p>A brownfield React + Node.js task-management app demonstrating a full AI-assisted Software Development Lifecycle (SDLC) powered by <strong>Claude Code CLI</strong> via <strong>CodeMie</strong>. Every phase is driven by specialised Claude agents with Human-in-the-Loop checkpoints.</p>
<h2>Documentation Pages</h2>
<table>
<tr><th>Page</th><th>Description</th></tr>
<tr><td><ac:link><ri:page ri:content-title="Architecture - Capstone" /></ac:link></td><td>System architecture, tech stack decisions, component diagram</td></tr>
<tr><td><ac:link><ri:page ri:content-title="HLD - High Level Design" /></ac:link></td><td>High-level design, data flow, API contracts, DB schema</td></tr>
<tr><td><ac:link><ri:page ri:content-title="FRD - Functional Requirements Document" /></ac:link></td><td>Functional requirements, user stories, acceptance criteria</td></tr>
<tr><td><ac:link><ri:page ri:content-title="API Reference - Capstone REST API" /></ac:link></td><td>All backend endpoints with request/response examples</td></tr>
<tr><td><ac:link><ri:page ri:content-title="Test Execution Report - E2E Playwright" /></ac:link></td><td>Test suite summary (61 tests), coverage, suites breakdown</td></tr>
<tr><td><ac:link><ri:page ri:content-title="Development and Deployment Guide" /></ac:link></td><td>Setup, run, build, environment variables, CI/CD</td></tr>
</table>
<h2>SDLC Phases</h2>
<table>
<tr><th>Phase</th><th>Agent</th><th>Artifact</th></tr>
<tr><td>1 - BA Analysis</td><td>ba-agent</td><td>Jira Epic + 5 Stories (55184-55188)</td></tr>
<tr><td>2 - Design</td><td>architect-agent</td><td>Architecture doc + HLD on Confluence</td></tr>
<tr><td>3 - Development</td><td>dev-agent</td><td>Feature commits (stories 55184-55188)</td></tr>
<tr><td>4 - Code Review</td><td>review-agent</td><td>Review findings table</td></tr>
<tr><td>5 - QA</td><td>qa-agent</td><td>61 Playwright E2E tests</td></tr>
<tr><td>6 - Build/Deploy</td><td>deploy-agent</td><td>npm run build, local verification</td></tr>
<tr><td>7 - Documentation</td><td>docs-agent</td><td>Confluence FRD + API docs + README</td></tr>
</table>
<h2>Jira Stories</h2>
<table>
<tr><th>Story</th><th>Title</th><th>Status</th></tr>
<tr><td><a href="https://jiraeu.epam.com/browse/EPMCDMETST-55183">EPMCDMETST-55183</a></td><td>[Epic] AI-Driven SDLC Enhancements</td><td>Open</td></tr>
<tr><td><a href="https://jiraeu.epam.com/browse/EPMCDMETST-55184">EPMCDMETST-55184</a></td><td>Item Management Dashboard UI</td><td>Resolved</td></tr>
<tr><td><a href="https://jiraeu.epam.com/browse/EPMCDMETST-55185">EPMCDMETST-55185</a></td><td>JWT Auth Guard and Protected Routes</td><td>Resolved</td></tr>
<tr><td><a href="https://jiraeu.epam.com/browse/EPMCDMETST-55186">EPMCDMETST-55186</a></td><td>Item Search and Status Filter</td><td>Resolved</td></tr>
<tr><td><a href="https://jiraeu.epam.com/browse/EPMCDMETST-55187">EPMCDMETST-55187</a></td><td>Item Status Update - Complete CRUD</td><td>Resolved</td></tr>
<tr><td><a href="https://jiraeu.epam.com/browse/EPMCDMETST-55188">EPMCDMETST-55188</a></td><td>Pagination for Items List</td><td>Resolved</td></tr>
</table>"""

payload = {
    "version": {"number": version + 1},
    "title": title,
    "type": "page",
    "body": {
        "storage": {
            "value": body,
            "representation": "storage"
        }
    }
}

with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False, encoding='utf-8') as f:
    json.dump(payload, f, ensure_ascii=False)
    fname = f.name

r2 = subprocess.run([
    'curl', '-s', '-X', 'PUT',
    f'{BASE}/rest/api/content/{HOME}',
    '-H', f'Authorization: Bearer {TOKEN}',
    '-H', 'Content-Type: application/json',
    '--data-binary', f'@{fname}'
], capture_output=True, text=True)
os.unlink(fname)

resp = json.loads(r2.stdout) if r2.stdout.strip() else {}
if resp.get('id'):
    print(f"OK updated Home page [{resp['id']}] v{resp['version']['number']}")
    print(f"   {BASE}/pages/viewpage.action?pageId={resp['id']}")
else:
    print(f"FAIL: {r2.stdout[:300]}")
