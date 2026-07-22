"""Update the 4 existing Confluence child pages with the latest content from push_confluence.py."""
import ast, json, os, re, subprocess, tempfile

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

# IDs discovered from the live Confluence space
PAGE_IDS = {
    'FRD - Functional Requirements Document':  '2889556181',
    'API Reference - Capstone REST API':        '2889556182',
    'Test Execution Report - E2E Playwright':   '2889556184',
    'Development and Deployment Guide':         '2889556185',
}

# Parse the pages list from push_confluence.py (avoids re-importing the executable script)
push_path = os.path.join(os.path.dirname(__file__), 'push_confluence.py')
with open(push_path, encoding='utf-8') as f:
    src = f.read()

m = re.search(r'^pages\s*=\s*(\[.*?\n\])', src, re.DOTALL | re.MULTILINE)
if not m:
    print('ERROR: Could not find pages list in push_confluence.py')
    raise SystemExit(1)

pages = ast.literal_eval(m.group(1))
print(f'Found {len(pages)} pages to update\n')

for p in pages:
    pid = PAGE_IDS.get(p['title'])
    if not pid:
        print(f'SKIP (no ID): {p["title"]}')
        continue

    payload = {
        'version': {'number': 2},
        'title': p['title'],
        'type': 'page',
        'body': {'storage': {'value': p['body'], 'representation': 'storage'}},
    }

    with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False, encoding='utf-8') as f:
        json.dump(payload, f, ensure_ascii=False)
        fname = f.name

    r = subprocess.run([
        'curl', '-s', '-X', 'PUT',
        f'{BASE}/rest/api/content/{pid}',
        '-H', f'Authorization: Bearer {TOKEN}',
        '-H', 'Content-Type: application/json',
        '--data-binary', f'@{fname}',
    ], capture_output=True, text=True)
    os.unlink(fname)

    try:
        resp = json.loads(r.stdout)
    except Exception:
        resp = {}

    if resp.get('id'):
        ver = resp['version']['number']
        print(f'UPDATED [{resp["id"]}] v{ver}  {p["title"]}')
        print(f'   {BASE}/pages/viewpage.action?pageId={resp["id"]}')
    else:
        print(f'FAIL  {p["title"]}')
        print(f'   {r.stdout[:300]}')
    print()
