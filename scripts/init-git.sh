#!/bin/bash
# Run once to initialize git repo and push to remote

set -e

echo "Initializing Git repository..."
git init
git add .
git commit -m "chore: initial project scaffold — AI-driven SDLC capstone"

echo ""
echo "Next steps:"
echo "  1. Create a repo on GitHub: https://github.com/new"
echo "  2. Run: git remote add origin <YOUR_REPO_URL>"
echo "  3. Run: git branch -M main"
echo "  4. Run: git push -u origin main"
