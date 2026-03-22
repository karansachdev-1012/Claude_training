# Git Glossary for Onboarding

Use these definitions when explaining git concepts to newcomers.

## Core Concepts

- **Commit** — A snapshot of changes. Think of it like a save point in a game.
- **Branch** — A parallel line of development. Like making a copy of your document to try something new without risking the original.
- **Merge** — Combining changes from one branch into another. Like accepting edits from a collaborator.
- **Rebase** — Replaying your commits on top of another branch. Makes history look cleaner but rewrites commit hashes.
- **HEAD** — The commit you're currently looking at. It's like "You Are Here" on a map.

## Common Branch Naming Conventions

| Prefix | Meaning | Example |
|--------|---------|---------|
| `main` / `master` | Production-ready code | `main` |
| `feat/` or `feature/` | New feature in progress | `feat/user-auth` |
| `fix/` or `bugfix/` | Bug fix | `fix/login-crash` |
| `docs/` | Documentation changes | `docs/update-readme` |
| `chore/` | Maintenance tasks | `chore/update-deps` |
| `release/` | Release preparation | `release/v2.1.0` |

## Reading a Git Log

```
a1b2c3d feat: add login page        ← commit hash + message
d4e5f6g fix: resolve null pointer   ← older commit below
```

- The **hash** (e.g., `a1b2c3d`) uniquely identifies each commit
- The **message** describes what changed
- Commits are listed newest-first (top = most recent)
