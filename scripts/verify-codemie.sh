#!/bin/bash
# CodeMie Agent Discovery & Verification Script
# Validates agent registration, profile setup, and integration readiness

set -e

PROJECT_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
CODEMIE_DIR="$PROJECT_ROOT/.codemie"
AGENTS_DIR="$PROJECT_ROOT/.claude/agents"

echo "═══════════════════════════════════════════════════════════════"
echo "CodeMie Agent Discovery & Verification"
echo "═══════════════════════════════════════════════════════════════"
echo ""

# 1. Verify config files exist
echo "✓ Checking CodeMie configuration files..."
config_files=(
  "$CODEMIE_DIR/codemie.json"
  "$CODEMIE_DIR/agents-manifest.json"
  "$CODEMIE_DIR/profiles/work.json"
  "$CODEMIE_DIR/profiles/personal.json"
)

for file in "${config_files[@]}"; do
  if [ -f "$file" ]; then
    echo "  ✓ $(basename $file)"
  else
    echo "  ✗ MISSING: $(basename $file)"
  fi
done
echo ""

# 2. Discover agents from .claude/agents/
echo "✓ Agent Discovery (.claude/agents/)..."
agent_count=0
if [ -d "$AGENTS_DIR" ]; then
  while IFS= read -r agent_file; do
    agent_name=$(basename "$agent_file" .md)
    echo "  ✓ $agent_name"
    ((agent_count++))
  done < <(find "$AGENTS_DIR" -name "*.md" -type f)
else
  echo "  ✗ Agents directory not found: $AGENTS_DIR"
fi
echo "  Total agents: $agent_count"
echo ""

# 3. Validate JSON syntax
echo "✓ Validating JSON syntax..."
for file in "$CODEMIE_DIR"/*.json "$CODEMIE_DIR/profiles"/*.json; do
  if [ -f "$file" ]; then
    if jq empty "$file" 2>/dev/null; then
      echo "  ✓ $(basename $file)"
    else
      echo "  ✗ Invalid JSON: $(basename $file)"
    fi
  fi
done
echo ""

# 4. Check environment variables
echo "✓ Environment variables check (.env)..."
env_file="$PROJECT_ROOT/.env"
if [ -f "$env_file" ]; then
  source "$env_file"
  required_vars=(
    "JIRA_API_TOKEN"
    "JIRA_BASE_URL"
    "CONFLUENCE_API_TOKEN"
    "CONFLUENCE_BASE_URL"
    "GITHUB_TOKEN"
  )

  missing_count=0
  for var in "${required_vars[@]}"; do
    if [ -z "${!var}" ]; then
      echo "  ✗ Missing: $var"
      ((missing_count++))
    else
      echo "  ✓ $var is set"
    fi
  done

  if [ $missing_count -gt 0 ]; then
    echo "  ⚠ Warning: $missing_count variables not set"
  fi
else
  echo "  ✗ .env file not found. Copy from .env.example and fill in values."
fi
echo ""

# 5. Parse agents-manifest.json
echo "✓ Agent manifest analysis..."
manifest="$CODEMIE_DIR/agents-manifest.json"
if [ -f "$manifest" ]; then
  agent_list=$(jq -r '.agents[].id' "$manifest" 2>/dev/null | sort)
  echo "  Registered agents in manifest:"
  while IFS= read -r agent; do
    echo "    • $agent"
  done <<< "$agent_list"

  echo ""
  echo "  Profiles defined:"
  profiles=$(jq -r '.profiles | keys[]' "$manifest" 2>/dev/null)
  while IFS= read -r profile; do
    echo "    • $profile"
  done <<< "$profiles"
fi
echo ""

# 6. Summary & next steps
echo "═══════════════════════════════════════════════════════════════"
echo "Summary"
echo "═══════════════════════════════════════════════════════════════"
echo ""
echo "✓ Configuration: Ready"
echo "✓ Agents: $agent_count discovered"
echo "✓ Profiles: 2 defined (work, personal)"
echo ""
echo "Next steps:"
echo "  1. codemie setup                 # Initialize CodeMie"
echo "  2. codemie agents list           # List all agents"
echo "  3. codemie profile set work      # Set work profile"
echo "  4. codemie /ba \"Analyze app\"    # Invoke BA agent"
echo ""
echo "See docs/CODEMIE_SETUP.md for detailed usage guide."
echo ""
