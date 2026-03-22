# Claude Training

A repository for training and customizing [Claude Code](https://docs.anthropic.com/en/docs/claude-code) with custom skills, agents, hooks, and MCP servers. It demonstrates all 5 Claude Code customization features working together.

## Features

- Auto-generate commit messages following conventional commit format
- Create full pull requests — push, describe, and open on GitHub in one step
- Regenerate README files with smart read-first-then-compare workflow
- Onboard new developers with a read-only codebase walkthrough
- Review skill files for quality using a custom subagent
- Read any webpage via the fetch MCP server
- Auto-generate `requirements.txt` from Python imports when updating the README
- Enforce project standards automatically via CLAUDE.md and hooks

## Project Structure

```
Claude_training/
├── CLAUDE.md                              # Always-on project rules (loaded every conversation)
├── .mcp.json                              # MCP server config (fetch — web page reader)
├── README.md
├── example.py                             # Sample Flask app (demonstrates requirements.txt hook)
├── requirements.txt                       # Auto-generated from Python imports by hook
└── .claude/
    ├── settings.local.json                # Hooks (auto-reminders + requirements.txt generation)
    ├── hooks/
    │   └── update-requirements.py         # Scans Python imports → generates requirements.txt
    ├── agents/
    │   └── code-reviewer.md               # Custom subagent for reviewing skills
    └── skills/
        ├── commit/
        │   └── SKILL.md                   # Auto-generates commit messages
        ├── pr-description/
        │   └── SKILL.md                   # Full PR flow: push + describe + create
        ├── update-readme/
        │   └── SKILL.md                   # Smart README updates
        └── git-onboarding/
            ├── SKILL.md                   # Read-only codebase walkthrough
            ├── scripts/
            │   └── repo-summary.sh        # Outputs repo snapshot (run, don't read)
            ├── references/
            │   ├── git-glossary.md        # Beginner-friendly git definitions
            │   └── onboarding-checklist.md # Ensures full onboarding coverage
            └── assets/
                └── onboarding-template.md # Response template for walkthroughs
```

## How It All Works Together

This repo uses all 5 Claude Code customization features. Each one solves a different problem:

### CLAUDE.md — Always-On Rules

- **What:** Project-wide standards loaded into every conversation automatically
- **When:** Rules that apply all the time, regardless of what task you're doing
- **Flow:** You start a conversation → Claude reads `CLAUDE.md` → rules apply to everything Claude does

**Current rules in this repo:**
```
- Always use conventional commit format (feat:, fix:, docs:, etc.)
- Never commit secrets (.env, credentials, API keys)
- Keep skill files under 500 lines
- Never force push to main
- Branch naming: feat/, fix/, docs/, chore/ prefixes
```

### Skills — On-Demand Expertise

- **What:** Task-specific instructions that load only when triggered by a phrase or slash command
- **When:** You say a trigger phrase like "commit" or type `/commit`
- **Flow:** You say "commit my work" → Claude matches it to the commit skill → loads `SKILL.md` → follows the step-by-step instructions inside

**Why not put everything in CLAUDE.md?** Because your PR review checklist doesn't need to be in context when you're writing new code. Skills keep context lean by loading only what's needed.

### Hooks — Event-Driven Automation

- **What:** Shell commands that run automatically when certain events happen
- **When:** Fires after tool calls, file saves, or other events — you don't trigger these manually
- **Flow:** Claude edits a file → `PostToolUse` hook fires → runs the command → you see the output

**Current hooks in this repo:**
```json
{
  "hooks": {
    "PreToolUse": [{
      "matcher": "Skill",
      "hooks": [{
        "type": "command",
        "command": "python .claude/hooks/update-requirements.py"
      }]
    }],
    "PostToolUse": [{
      "matcher": "Write|Edit",
      "hooks": [{
        "type": "command",
        "command": "echo '✓ File modified — remember to test your changes'"
      }]
    }]
  }
}
```

Two hooks are active:
1. **PreToolUse → Skill**: Before any skill runs, `update-requirements.py` checks if it's the `update-readme` skill. If so, it scans all Python files for imports and generates/updates `requirements.txt` using `pipreqs` (with a manual fallback). This ensures the README always reflects current dependencies.
2. **PostToolUse → Write|Edit**: Every time Claude writes or edits a file, you get a reminder to test your changes.

### MCP Servers — External Tools

- **What:** Gives Claude access to tools outside the codebase (web, APIs, databases)
- **When:** Claude needs to reach something external — like reading a webpage
- **Flow:** You ask "read this URL and summarize it" → Claude calls the fetch MCP → MCP server downloads the page → content returned to Claude → Claude explains it

**Current MCP in this repo:**
```json
{
  "mcpServers": {
    "fetch": {
      "type": "stdio",
      "command": "python",
      "args": ["-m", "uv", "tool", "run", "mcp-server-fetch"]
    }
  }
}
```

**Lifecycle:** The MCP server starts automatically when Claude Code launches and runs as a background process for the entire session. When you close Claude Code, the process is killed automatically. You never need to manually stop it. If it crashes mid-session, Claude Code restarts it on the next call.

**Prerequisites:** Requires Python and [uv](https://docs.astral.sh/uv/) installed. The fetch MCP server is installed on-demand via `uv tool run`.

### Custom Agents — Delegated Work with Skills

- **What:** Subagents that run in isolated contexts with specific skills loaded
- **When:** You want to delegate a task to a separate worker with its own tool access and expertise
- **Flow:** You say "use the code-reviewer agent to review my skills" → agent starts with fresh context → loads its listed skills → does its work → returns results

**Current agent in this repo:**
```yaml
name: code-reviewer
tools: Read, Glob, Grep          # Read-only — can't edit anything
model: sonnet                     # Uses faster/cheaper model
skills: git-onboarding, commit    # Only these 2 skills are loaded
```

**Important:** Built-in agents (Explorer, Plan) CANNOT access your skills. Only custom agents defined in `.claude/agents/` can, and you must explicitly list which skills they get in the `skills:` field.

## Skills Reference

| Skill Name | What It Does | How to Invoke |
|------------|--------------|---------------|
| **commit** | Commits all staged and unstaged changes with an auto-generated message using conventional commit format. Skips secret files automatically. | `/commit`, "commit", "save changes", "commit my work", "make a commit" |
| **pr-description** | Creates a full pull request end to end — pushes the branch, generates a description, and opens the PR on GitHub. | `/pr-description`, "create a PR", "open a PR", "make a pull request", "push and create PR", "submit a PR" |
| **update-readme** | Reads existing README, compares it to the current repo state, and updates only what's changed. Documents all features including skills, agents, hooks, and MCP. | `/update-readme`, "update the readme", "regenerate the readme", "refresh project documentation" |
| **git-onboarding** | Read-only guide that walks through the README, codebase structure, code flow, and git history. Uses progressive disclosure — glossary, checklist, and template load only when needed. | `/git-onboarding`, "onboard me", "explain the project", "how does the code work?", "walk me through the codebase", "what does this repo do?", "explain the branches" |

## Agents Reference

| Agent Name | What It Does | Tools | Skills Loaded |
|------------|--------------|-------|---------------|
| **code-reviewer** | Reviews skill files for quality, completeness, and best practices. Checks frontmatter, trigger phrases, progressive disclosure, and security. | Read, Glob, Grep | git-onboarding, commit |

## Getting Started

### Prerequisites

- [Claude Code](https://docs.anthropic.com/en/docs/claude-code) installed
- [Python](https://www.python.org/) and [uv](https://docs.astral.sh/uv/) (required for the fetch MCP server and the requirements.txt hook)
- [GitHub CLI](https://cli.github.com/) (`gh`) installed and authenticated (required for the PR skill)

### Usage

Skills and agents are automatically available when working in this repository. Invoke them in two ways:

1. **Slash command** — type the skill name directly:
   ```
   /commit
   /pr-description
   /update-readme
   /git-onboarding
   ```

2. **Natural language** — just ask Claude using any trigger phrase:
   ```
   "commit my work"
   "create a PR"
   "update the readme"
   "onboard me"
   ```

3. **Agents** — ask Claude to use a specific agent:
   ```
   "use the code-reviewer agent to review my skills"
   ```
