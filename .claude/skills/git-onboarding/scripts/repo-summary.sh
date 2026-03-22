#!/bin/bash
# Generates a quick snapshot of the repo's git health and activity.
# Claude runs this script (doesn't read it) — only the output goes into context.

echo "=== REPO SUMMARY ==="
echo ""

echo "--- Branches ---"
git branch -a --format='%(refname:short)  %(objectname:short)  %(committerdate:relative)' 2>/dev/null
echo ""

echo "--- Contributors ---"
git shortlog -sn --all 2>/dev/null
echo ""

echo "--- Recent Commits (last 10) ---"
git log --oneline --all --graph -10 2>/dev/null
echo ""

echo "--- File Count by Extension ---"
git ls-files | grep -oE '\.[^.]+$' | sort | uniq -c | sort -rn 2>/dev/null
echo ""

echo "--- Repo Age ---"
FIRST=$(git log --reverse --format='%ci' | head -1 2>/dev/null)
LATEST=$(git log -1 --format='%ci' 2>/dev/null)
echo "First commit: $FIRST"
echo "Latest commit: $LATEST"
