---
name: update-readme
description: Updates the README.md file. Use when the user asks to update the readme, update the readme file, regenerate the readme, or refresh project documentation.
---

When updating the README:

1. **Read the existing README.md first** — understand what's already there before making changes. Never start from scratch unless the file doesn't exist.

2. **Analyze the repository** by doing ALL of the following:
   - List all top-level files and directories
   - Read key config files (package.json, pyproject.toml, Cargo.toml, go.mod, Makefile, docker-compose.yml, etc.) to understand the tech stack, dependencies, and scripts
   - Scan `src/`, `lib/`, `app/`, or equivalent directories to understand the project structure
   - Check for existing docs/, examples/, or tests/ directories
   - Read ALL skill files in `.claude/skills/*/SKILL.md` to understand available skills, their descriptions, and trigger phrases
   - Run `git log --oneline -20` to understand recent activity and project purpose

3. **Compare what the README says vs what the repo actually contains**:
   - Are there new files, folders, or skills that the README doesn't mention?
   - Are there sections in the README that reference things that no longer exist?
   - Has the project structure changed since the README was last updated?
   - Are there new dependencies, scripts, or commands not documented?

4. **Update the README.md** to include all applicable sections:

   - **Project title and description**: Clear, concise explanation of what the project does and why it exists
   - **Features**: Key features or capabilities as bullet points
   - **Tech Stack**: Languages, frameworks, and major dependencies
   - **Project Structure**: Tree or table showing the directory layout and what each part does — must reflect the **current** file tree, not an outdated one
   - **Getting Started**:
     - Prerequisites (runtime versions, tools needed)
     - Installation steps
     - Configuration / environment variables (if any)
   - **Usage**: How to run the project, example commands, or code snippets
   - **Scripts / Commands**: Table of available npm scripts, make targets, or CLI commands
   - **Testing**: How to run tests
   - **Skills Reference**: For each skill found in `.claude/skills/`, create a table with columns: **Skill Name**, **What It Does** (one-line summary), and **How to Invoke** (list the trigger phrases and slash commands that activate it — pull these from the skill's `description` field and any slash command patterns like `/skill-name`)
   - **Contributing**: Brief contribution guidelines if applicable
   - **License**: License info if a LICENSE file exists

5. **Guidelines**:
   - Only include sections that are relevant — skip empty or inapplicable ones
   - Use clear markdown formatting with headers, code blocks, and tables
   - Keep descriptions accurate to what the code actually does — do not fabricate features
   - If the repo is small or new, keep the README proportionally brief but still well-structured
   - Preserve any existing content that is still accurate — only update or replace parts that are outdated or incomplete
   - When adding new sections, place them in a logical order relative to existing ones
   - After writing, re-read the final README to make sure it's consistent and nothing is duplicated or contradictory
