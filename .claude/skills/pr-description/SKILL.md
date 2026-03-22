---
name: pr-description
description: Creates a full pull request — pushes the branch, generates a description, and opens the PR on GitHub. Use when the user says "create a PR", "open a PR", "make a pull request", "push and create PR", or "submit a PR".
---

When creating a pull request, handle the **entire process** end to end:

## Step 1 — Check the current state

Run all of these to understand what you're working with:

- `git status` — check for uncommitted changes (warn the user if there are any)
- `git branch --show-current` — get the current branch name
- `git log main..HEAD --oneline` — see all commits that will be in the PR
- `git diff main...HEAD --stat` — summary of files changed vs main

If the current branch is `main`, stop and tell the user they need to be on a feature branch.

## Step 2 — Push the branch

- Check if the branch has an upstream: `git rev-parse --abbrev-ref @{upstream}`
- If not, push with: `git push -u origin <branch-name>`
- If it does, check if local is ahead of remote and push if needed

## Step 3 — Generate the PR description

Analyze all commits and diffs (not just the latest commit — ALL changes on the branch), then write a description:

### Title
- Keep under 70 characters
- Use imperative mood: "Add feature" not "Added feature"
- Be specific: "Add git-onboarding skill" not "Update skills"

### Body format
```
## What
One sentence explaining what this PR does.

## Why
Brief context on why this change is needed.

## Changes
- Bullet points of specific changes made
- Group related changes together
- Mention any files added, deleted, or renamed
```

## Step 4 — Create the PR

Use `gh pr create` to open the PR on GitHub:

- Set the base branch to `main`
- Pass the title with `--title`
- Pass the body using a HEREDOC for proper formatting
- After creation, output the PR URL so the user can click it

## Step 5 — Report back

Show the user:
- The PR URL
- The title and a brief summary of what's in it
- Number of commits and files changed
