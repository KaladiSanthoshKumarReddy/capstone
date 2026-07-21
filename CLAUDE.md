# Capstone: AI-Assistant Driven SDLC

## Project
AI-powered SDLC pipeline for a brownfield React + Node.js app.
Project in Jira: **EPMCDMETST** | Group: **mm-learning-group-1**

## Stack
- **Frontend**: React 18 + TypeScript + Vite
- **Backend**: Node.js + Express + TypeScript
- **Database**: SQLite (via better-sqlite3)
- **Testing**: Playwright TypeScript (E2E) + Vitest (unit)
- **CI**: GitHub Actions

## Integrations
- Jira: https://jiraeu.epam.com  (env: JIRA_BASE_URL, JIRA_API_TOKEN)
- Confluence: https://kb.epam.com (env: CONFLUENCE_BASE_URL, CONFLUENCE_API_TOKEN)
- Git: https://github.com/KaladiSanthoshKumarReddy/capstone (branch: main)

## Agents available (in .claude/agents/)
| Agent | Role |
|-------|------|
| ba-agent | Business Analyst — writes Jira epics/stories from requirements |
| architect-agent | Creates architecture docs, HLD/LLD, pushes to Confluence |
| dev-agent | Generates React + Node.js code, commits to Git |
| qa-agent | Writes Gherkin + Playwright TS tests |
| review-agent | Code reviews PRs, posts comments to Git |
| deploy-agent | Runs build scripts, deploys locally |
| docs-agent | Updates Confluence pages with FRD/design docs |

## Commands
```bash
# Start frontend dev server
cd frontend && npm run dev

# Start backend
cd backend && npm run dev

# Run E2E tests
cd tests && npx playwright test

# Run all (full SDLC demo)
npm run sdlc
```

## Environment
Copy `.env.example` to `.env` and fill in values before running.
