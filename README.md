# Claude Training

A repository for training and customizing [Claude Code](https://docs.anthropic.com/en/docs/claude-code) with custom skills.

## Custom Skills

This project includes reusable Claude Code skills located in `.claude/skills/`:

| Skill | Description |
|-------|-------------|
| **commit** | Commits all changes with an auto-generated descriptive message using conventional commit format (`feat:`, `fix:`, `docs:`, etc.). Skips secret files automatically. |
| **pr-description** | Generates pull request descriptions by analyzing branch diffs. Outputs a structured summary with What, Why, and Changes sections. |
| **update-readme** | Analyzes the repository and generates or updates a comprehensive README.md with relevant sections based on actual project contents. |

## Project Structure

```
.claude/
  skills/
    commit/            # Skill for auto-generating commit messages
    pr-description/    # Skill for writing PR descriptions
    update-readme/     # Skill for auto-generating README files
```

## Usage

These skills are automatically available in Claude Code when working in this repository:

- **Commit** — invoke with `/commit` or ask Claude to commit your changes
- **PR descriptions** — invoke with `/pr-description` or ask Claude to summarize changes for a PR
- **Update README** — invoke with `/update-readme` or ask Claude to update the readme
