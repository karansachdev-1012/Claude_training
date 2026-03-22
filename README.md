# Claude Training

A repository for training and customizing [Claude Code](https://docs.anthropic.com/en/docs/claude-code) with custom skills — reusable instruction files that teach Claude how to perform specific tasks.

## Features

- Auto-generate commit messages following conventional commit format
- Write structured pull request descriptions from branch diffs
- Regenerate README files based on actual project contents
- Onboard new developers with a read-only codebase walkthrough

## Project Structure

```
.claude/
  skills/
    commit/                        # Auto-generates commit messages
      SKILL.md
    pr-description/                # Writes PR descriptions
      SKILL.md
    update-readme/                 # Generates/updates README files
      SKILL.md
    git-onboarding/                # Read-only codebase onboarding guide
      SKILL.md
      scripts/
        repo-summary.sh            # Outputs repo snapshot (branches, contributors, stats)
      references/
        git-glossary.md            # Beginner-friendly git definitions
        onboarding-checklist.md    # Checklist to ensure full coverage during onboarding
      assets/
        onboarding-template.md    # Response template for full walkthrough requests
```

## Skills Reference

| Skill Name | What It Does | How to Invoke |
|------------|--------------|---------------|
| **commit** | Commits all staged and unstaged changes with an auto-generated descriptive message using conventional commit format. Skips secret files automatically. | `/commit`, "commit", "save changes", "commit my work", "make a commit" |
| **pr-description** | Generates a pull request description by analyzing branch diffs. Outputs a structured summary with What, Why, and Changes sections. | `/pr-description`, "write a PR description", "summarize changes for a pull request" |
| **update-readme** | Analyzes the repository and generates or updates a comprehensive README with relevant sections based on actual project contents. | `/update-readme`, "update the readme", "regenerate the readme", "refresh project documentation" |
| **git-onboarding** | Read-only guide that explains the README, codebase structure, code flow, git history, and branches. Never modifies files. | `/git-onboarding`, "onboard me", "explain the project", "how does the code work?", "walk me through the codebase", "what does this repo do?", "explain the flow", "what's the git history?", "explain the branches" |

## Usage

These skills are automatically available in Claude Code when working in this repository. You can invoke them in two ways:

1. **Slash command** — type the skill name directly (e.g., `/commit`)
2. **Natural language** — just ask Claude using any of the trigger phrases listed in the table above
