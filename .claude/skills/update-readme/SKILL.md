---
name: update-readme
description: Updates the README.md file. Use when the user asks to update the readme, update the readme file, regenerate the readme, or refresh project documentation.
---

When updating the README:

## Step 1 — Read existing README

Read the existing `README.md` first. Understand what's already there before making changes. Never start from scratch unless the file doesn't exist.

## Step 2 — Analyze the full repository

Scan everything to understand the current state:

- List all top-level files and directories
- Read key config files (package.json, pyproject.toml, Cargo.toml, go.mod, Makefile, docker-compose.yml, etc.)
- Scan `src/`, `lib/`, `app/`, or equivalent directories
- Check for docs/, examples/, or tests/ directories
- Read ALL skill files in `.claude/skills/*/SKILL.md`
- Read ALL agent files in `.claude/agents/*.md`
- Read `CLAUDE.md` if it exists
- Read `.mcp.json` if it exists
- Read `.claude/settings.local.json` for hooks
- Run `git log --oneline -20` to understand recent activity

## Step 3 — Compare README vs reality

Before writing, check what's outdated:

- Are there new files, folders, skills, or agents that the README doesn't mention?
- Are there sections referencing things that no longer exist?
- Has the project structure changed?
- Are there new MCP servers, hooks, or agents not documented?

## Step 4 — Write the README

Include all applicable sections in this order:

### Required sections

- **Project title and description**: What the project does and why it exists
- **Features**: Key capabilities as bullet points

### Structure sections

- **Project Structure**: Tree showing the directory layout — must match the CURRENT file tree. Include ALL of these if they exist:
  - `.claude/skills/` — each skill folder and its contents
  - `.claude/agents/` — each agent file
  - `CLAUDE.md`
  - `.mcp.json`
  - `.claude/settings.local.json`

### How It All Works Together

Include a section that explains the 5 customization features and how they connect. Use this structure:

**CLAUDE.md (Always-on rules)**
- What: Project-wide standards loaded into every conversation
- When: Rules that apply all the time, regardless of task
- Example from repo: show what's in the current CLAUDE.md
- Flow: User starts conversation → Claude reads CLAUDE.md → rules apply to everything Claude does

**Skills (On-demand expertise)**
- What: Task-specific instructions loaded only when triggered
- When: User says a trigger phrase or slash command
- Example from repo: list each skill with its triggers
- Flow: User says "commit" → Claude matches to commit skill → loads SKILL.md → follows instructions

**Hooks (Event-driven automation)**
- What: Commands that run automatically when certain events happen
- When: After tool calls, file saves, or other events
- Example from repo: show the current hook config
- Flow: Claude edits a file → PostToolUse hook fires → runs the echo command → user sees reminder

**MCP Servers (External tools)**
- What: Gives Claude access to tools outside the codebase
- When: Claude needs to reach external services (web, APIs, databases)
- Example from repo: show the current .mcp.json config
- Flow: User asks "read this URL" → Claude calls fetch MCP → MCP server downloads page → content returned to Claude
- Lifecycle: The MCP server starts automatically when Claude Code launches. It runs as a background process for the duration of the session. When you close Claude Code, the process is killed automatically. You do NOT need to manually stop it. If it crashes, Claude Code restarts it on the next call.

**Custom Agents (Delegated work with skills)**
- What: Subagents that run in isolated contexts with specific skills loaded
- When: You want to delegate a task to a separate worker with its own tool access
- Example from repo: show the current agent config
- Flow: User says "use code-reviewer agent" → agent starts with fresh context → loads listed skills → does its work → returns results
- Important: Built-in agents (Explorer, Plan) CANNOT use skills. Only custom agents in `.claude/agents/` can, and you must list skills explicitly in the `skills:` field.

### Skills Reference

For each skill in `.claude/skills/`, create a table:

| Skill Name | What It Does | How to Invoke |
|---|---|---|
| **name** | one-line summary from description | `/slash-command`, "trigger phrase 1", "trigger phrase 2" |

Pull trigger phrases from each skill's `description` field.

### Agents Reference

For each agent in `.claude/agents/`, create a table:

| Agent Name | What It Does | Tools | Skills Loaded |
|---|---|---|---|
| **name** | summary from description | tools list | skills list |

### Getting Started / Usage

- Prerequisites (Node.js for MCP, Claude Code installed)
- How to invoke skills (slash commands and natural language)
- How to invoke agents

## Step 5 — Guidelines

- Only include sections that are relevant — skip empty ones
- Use clear markdown formatting with headers, code blocks, and tables
- Keep descriptions accurate — do not fabricate features
- If the repo is small, keep the README proportionally brief
- Preserve existing content that is still accurate
- After writing, re-read the final README for consistency — no duplicates, no contradictions
