---
name: commit
description: Commits all staged and unstaged changes with an auto-generated descriptive commit message. Use when the user asks to commit, save changes, commit my work, or make a commit.
---

When committing changes:

1. **Analyze the changes** by running all of the following:
   - `git status` to see all modified, added, and deleted files
   - `git diff` to see unstaged changes
   - `git diff --cached` to see already-staged changes
   - `git log --oneline -5` to understand recent commit message style and context

2. **Stage the changes**:
   - Add all relevant changed files by name (prefer `git add <file>...` over `git add -A`)
   - Do NOT stage files that likely contain secrets (`.env`, `credentials.json`, API keys, tokens)
   - If secret files are detected, warn the user and skip them

3. **Generate a commit message** following these rules:
   - Use a short imperative subject line (max 72 characters) — e.g., "Add user auth endpoint" not "Added user auth endpoint"
   - Classify the change type: `feat`, `fix`, `refactor`, `docs`, `chore`, `test`, `style`
   - Format: `<type>: <concise description>`
   - If the change is non-trivial, add a blank line followed by a brief body explaining **why** the change was made
   - Match the tone and conventions of recent commits in the repo when possible

4. **Commit the changes**:
   - Use a HEREDOC to pass the commit message to avoid shell escaping issues
   - Run `git status` after committing to verify success

5. **Report back** with the commit hash and message summary
