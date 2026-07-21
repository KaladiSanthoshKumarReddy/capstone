# AI-Driven SDLC Step-by-Step Guide
## Capstone Project — mm-learning-group-1

---

## Prerequisites

Install these before starting:
```bash
node --version   # need v20+
npm --version    # need v10+
git --version
```

Install CodeMie CLI:
```bash
npm install -g @epam/codemie-cli
codemie login     # authenticate with your EPAM SSO
```

Install Claude Code CLI:
```bash
npm install -g @anthropic-ai/claude-code
claude --version
```

---

## Phase 0 — Project Setup (One-time)

```bash
# 1. Navigate to capstone folder
cd capstone/

# 2. Copy and fill in environment variables
cp .env.example .env
# Edit .env with your Jira PAT, Confluence PAT

# 3. Install all dependencies
npm run install:all

# 4. Initialize Git
bash scripts/init-git.sh
# Then create a GitHub repo and push

# 5. Start Claude Code CLI inside capstone/
claude
```

---

## Phase 1 — Analysis & Requirements (BA Agent)

**Goal**: Identify 3–5 enhancements for the app and create Jira stories.

In Claude Code CLI, type:
```
Analyze the existing app in frontend/src/ and backend/src/. 
Identify 5 feature gaps or enhancements. 
Create a Jira Epic and one Story per enhancement in project EPMCDMETST.
```

The **ba-agent** will:
1. Read your existing source code
2. Identify gaps (e.g. missing search, no pagination, no auth refresh, etc.)
3. Create Epic `[Capstone] AI-Driven SDLC Enhancements`
4. Create 5 Stories with full acceptance criteria in Jira
5. Print a table with Jira links and ask for **Human Review**

**Human-in-the-Loop (HITL) checkpoint**: Review stories in Jira, edit if needed, then tell Claude: `Stories approved, proceed to design`.

---

## Phase 2 — Design (Architect Agent)

**Goal**: Create Architecture, HLD, LLD, Wireframes → push to Confluence.

```
Create an architecture document for the capstone React + Node.js app.
Include system overview, component diagram, sequence diagrams, and data model.
Push to Confluence under the Capstone space.
```

The **architect-agent** will:
1. Generate architecture document with Mermaid diagrams
2. Write HLD (system components, tech stack justification)
3. Write LLD (per-feature: component tree, API contract, DB schema)
4. Push all to Confluence

**HITL checkpoint**: Review Confluence pages, approve, then say `Design approved, start coding`.

---

## Phase 3 — Development (Dev Agent)

**Goal**: Implement features story-by-story, commit to Git.

For each Jira story (e.g. EPMCDMETST-55166):
```
Implement story EPMCDMETST-55166: <story title>.
Create the React component and Express API endpoint.
Commit with the story key in the message.
```

The **dev-agent** will:
1. Read the Jira story
2. Implement React component in `frontend/src/`
3. Implement Express endpoint in `backend/src/`
4. Add SQLite migration if needed
5. Commit: `feat(scope): <description> [EPMCDMETST-55166]`
6. Ask for human review before opening PR

**HITL checkpoint**: Review the diff (`git diff main...HEAD`), approve, say `Code approved, open a PR`.

---

## Phase 4 — Code Review (Review Agent)

**Goal**: AI code review on the PR, inline comments on GitHub.

```
Review the code changes on the current branch against main.
Check for correctness, TypeScript issues, missing tests, security issues.
Post findings as PR comments.
```

The **review-agent** will:
1. Run `git diff main...HEAD`
2. Check against the review checklist (correctness, types, tests, security)
3. Post findings table
4. Either approve or request changes

**HITL checkpoint**: Developer addresses review findings, pushes fixes.

---

## Phase 5 — Testing (QA Agent)

**Goal**: Write Gherkin feature files + Playwright TS E2E tests, run them, store results.

```
Write Playwright TypeScript E2E tests for the features implemented in the last sprint.
Cover the happy path and at least one error scenario per feature.
Run the tests and save the HTML report.
```

The **qa-agent** will:
1. Read implemented React components for `data-testid` attributes
2. Write `.feature` files in `tests/features/`
3. Write Playwright specs in `tests/e2e/specs/`
4. Run: `cd tests && npx playwright test`
5. Save report to `tests/playwright-report/`
6. Commit test files with story key

**HITL checkpoint**: Review test report, approve, say `Tests passed, proceed to deployment`.

---

## Phase 6 — Build & Deployment

**Goal**: Build artifacts, deploy locally, verify the app runs.

```bash
# Build
npm run build

# Start locally (both frontend + backend)
npm run dev

# Verify
open http://localhost:3000
```

Build scripts committed to Git:
```bash
git add package.json frontend/package.json backend/package.json
git commit -m "chore(build): add build scripts for local deployment"
```

**HITL checkpoint**: Demo the running app end-to-end.

---

## Phase 7 — Documentation (Docs Agent)

**Goal**: Update Confluence with FRD, design docs, test results. Update README.

```
Update the Confluence capstone space with the FRD, architecture, test results.
Update the project README with setup instructions and all relevant links.
```

The **docs-agent** will:
1. Push FRD to Confluence
2. Push test execution results page
3. Update README.md with setup, run instructions, and Confluence links

---

## Demo Flow Checklist

| Step | Tool | HITL? | Artifact |
|------|------|-------|----------|
| 1. Gap Analysis | Claude Code + ba-agent | ✅ Review stories in Jira | Jira Epic + Stories |
| 2. Plan/Design | architect-agent + Confluence | ✅ Review design docs | Architecture doc, HLD, LLD |
| 3. Code Generation | dev-agent + Git | ✅ Review diff, approve PR | Feature branch + commits |
| 4. Code Review | review-agent + GitHub | ✅ Address findings | PR review comments |
| 5. Test | qa-agent + Playwright | ✅ Review test report | `.feature` + `.spec.ts` + HTML report |
| 6. Deploy | `npm run dev` | ✅ Demo the app | Running local app |
| 7. Docs | docs-agent + Confluence | ✅ Review doc pages | Confluence pages + README |

---

## Useful Claude Code CLI Prompts

```bash
# Start a session in the capstone folder
cd capstone && claude

# Phase 1 — BA
> analyze the app and create Jira stories for 5 enhancements in EPMCDMETST

# Phase 2 — Design
> create architecture document and push to Confluence

# Phase 3 — Dev (per story)
> implement story EPMCDMETST-55166

# Phase 4 — Review
> review the code changes on this branch

# Phase 5 — QA
> write Playwright tests for the login and dashboard features

# Phase 6 — Build
> build the project and verify it runs locally

# Phase 7 — Docs
> update Confluence with the full project documentation and update README
```

---

## Jira Ticket Structure

```
EPIC: [Capstone] AI-Driven SDLC Enhancements
├── Story: [Enhancement] Add search functionality
│   └── Task: Implement backend search endpoint
│   └── Task: Implement frontend search UI
│   └── Task: Write Playwright tests for search
├── Story: [Enhancement] Add pagination
├── Story: [Enhancement] Add user profile page
├── Story: [Enhancement] Add item filtering
└── Story: [Enhancement] Add export to CSV
```

---

## Confluence Space Structure

```
Capstone (mm-learning-group-1)
├── FRD — Functional Requirements Document
├── Architecture Overview (Mermaid diagrams)
├── High-Level Design
├── Low-Level Design
├── Wireframes
├── Test Plan
├── Test Execution Results (Playwright HTML report embedded)
└── Deployment Guide
```
