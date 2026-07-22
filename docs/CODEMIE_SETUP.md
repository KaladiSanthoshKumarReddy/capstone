# CodeMie CLI Integration Guide

> **Project:** Capstone — AI-Driven SDLC | **Group:** mm-learning-group-1

This guide explains how to use CodeMie CLI to invoke your 7 specialized agents for the complete SDLC workflow.

---

## Quick Setup

### 1. Initial CodeMie Setup
```bash
codemie setup
```
- Select provider: **Claude**
- Choose model: **claude-opus-4-7** (for work profile)
- Authenticate with your Claude API key or CodeMie SSO

### 2. Load Project Configuration
CodeMie auto-discovers your agents from `.codemie/codemie.json` and `.codemie/agents-manifest.json`:
```bash
cd capstone
codemie config show
```

### 3. Verify Agent Discovery
```bash
codemie agents list
```
**Expected output:**
```
✓ ba-agent          — Business Analyst
✓ architect-agent   — Architect  
✓ dev-agent         — Developer
✓ qa-agent          — QA Engineer
✓ review-agent      — Code Reviewer
✓ docs-agent        — Documentation Specialist
```

---

## Usage: Profile-Based Workflows

### **Work Profile** (Full SDLC — all 7 agents)
```bash
codemie profile set work
```
Includes: BA, Architect, Dev, QA, Review, Docs + Jira, Confluence, GitHub integrations

### **Personal Profile** (Dev-focused — 3 agents)
```bash
codemie profile set personal
```
Includes: Dev, QA, Docs agents + GitHub only (lightweight, faster)

### **View Current Profile**
```bash
codemie profile show
```

---

## Invoking Agents

### **Option 1: Slash Commands (Interactive)**
```bash
codemie /ba "Analyze the current app and identify 3 enhancement opportunities"
codemie /architect "Design the auth system HLD"
codemie /dev "Implement the search feature"
codemie /qa "Write Playwright tests for login flow"
codemie /review "Review the PR for EPMCDMETST-55184"
codemie /docs "Update Confluence with API documentation"
```

### **Option 2: Direct Agent Invocation**
```bash
codemie run ba-agent --prompt "Analyze requirements for the dashboard"
codemie run dev-agent --prompt "Create the ItemCard component"
codemie run qa-agent --prompt "Generate BDD scenarios for item CRUD"
```

### **Option 3: Interactive Agent Menu**
```bash
codemie agents
```
Select agent → Enter prompt → Agent executes with active profile settings

---

## Full SDLC Workflow (Work Profile)

### Phase 1 — BA Analysis
```bash
codemie profile set work
codemie /ba "Analyze frontend and backend. Identify 3–5 enhancements. Create Jira Epic + Stories."
```
**Output:** Jira Epic EPMCDMETST-XXXXX with 5 linked Stories

### Phase 2 — Design
```bash
codemie /architect "Create HLD for the recommended enhancements. Push to Confluence."
```
**Output:** Architecture doc on Confluence

### Phase 3 — Development
```bash
codemie /dev "Implement story EPMCDMETST-55184: Item Management Dashboard UI"
```
**Output:** Git commits on `main` branch

### Phase 4 — Code Review
```bash
codemie /review "Review PR #123 for EPMCDMETST-55184"
```
**Output:** Review comments on GitHub PR

### Phase 5 — QA
```bash
codemie /qa "Write Playwright E2E tests for item CRUD operations"
```
**Output:** Test specs in `tests/e2e/specs/`

### Phase 6 — Documentation
```bash
codemie /docs "Update Confluence FRD page with finalized requirements"
```
**Output:** Confluence page updated

---

## Configuration Reference

### `.codemie/codemie.json`
Main project config — project metadata, agent directory, integrations

### `.codemie/agents-manifest.json`
Agent registry — name, role, capabilities, dependencies, profile availability

### `.codemie/profiles/work.json`
Work profile — full SDLC with Jira, Confluence, GitHub enabled

### `.codemie/profiles/personal.json`
Personal profile — dev-focused, GitHub only, fewer agents

---

## Environment Variables

Required in `.env`:

| Variable | Profile | Purpose |
|----------|---------|---------|
| `JIRA_API_TOKEN` | work | Jira API authentication |
| `JIRA_BASE_URL` | work | Jira instance URL |
| `CONFLUENCE_API_TOKEN` | work | Confluence API authentication |
| `CONFLUENCE_BASE_URL` | work | Confluence instance URL |
| `GITHUB_TOKEN` | work, personal | GitHub repo access |

**Setup:**
```bash
cp .env.example .env
# Edit .env and fill in your tokens
```

---

## Agent Capabilities Matrix

| Agent | BA | Architect | Dev | QA | Review | Docs |
|-------|----|-----------|----|----|---------|----|
| **Jira** | ✅ Epic/Story | — | — | — | — | — |
| **Confluence** | — | ✅ HLD/LLD | — | — | — | ✅ FRD/API |
| **GitHub** | — | — | ✅ Commits | — | ✅ PR Comments | — |
| **Gherkin/BDD** | — | — | — | ✅ Scenarios | — | — |
| **Playwright TS** | — | — | — | ✅ E2E Tests | — | — |
| **Code Gen** | — | — | ✅ React/Node | — | — | — |
| **PR Review** | — | — | — | — | ✅ Comments | — |

---

## Troubleshooting

### Agents not discovered
```bash
codemie config scan
# Re-scans .claude/agents/ and updates manifest
```

### Missing dependencies
```bash
codemie profile validate
# Checks if required env vars are set and tokens valid
```

### Switch model for this run
```bash
codemie run ba-agent --model claude-sonnet-4-6 --prompt "..."
```

### Verbose logging
```bash
codemie run dev-agent --verbose --prompt "..."
```

### Clear cache
```bash
codemie cache clear
```

---

## Pro Tips

✅ **Use slash commands for speed** — `/dev "..."` is faster than typing full commands  
✅ **Chain agents** — Output from one agent can feed into the next  
✅ **Save prompts** — `codemie save-prompt <name>` for frequently used queries  
✅ **Profile switching** — `codemie profile set personal` for lightweight mode  
✅ **Test credentials** — `codemie auth test` before running agents that need integrations  

---

## Links

| Resource | URL |
|----------|-----|
| GitHub Repo | https://github.com/KaladiSanthoshKumarReddy/capstone |
| Jira Project | https://jiraeu.epam.com/browse/EPMCDMETST |
| Confluence Space | https://kb.epam.com/display/CAPSTONE |

**Human Review Required:** Verify CodeMie setup with `codemie agents list` before running full SDLC workflow.
