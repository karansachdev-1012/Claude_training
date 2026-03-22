---
name: update-readme
description: Updates the README.md file. Use when the user asks to update the readme, update the readme file, regenerate the readme, or refresh project documentation.
---

When updating the README:

1. **Analyze the repository** by doing ALL of the following:
   - List all top-level files and directories
   - Read key config files (package.json, pyproject.toml, Cargo.toml, go.mod, Makefile, docker-compose.yml, etc.) to understand the tech stack, dependencies, and scripts
   - Scan `src/`, `lib/`, `app/`, or equivalent directories to understand the project structure
   - Read existing README.md if it exists
   - Check for existing docs/, examples/, or tests/ directories
   - Run `git log --oneline -20` to understand recent activity and project purpose

2. **Write a comprehensive README.md** that includes all applicable sections:

   - **Project title and description**: Clear, concise explanation of what the project does and why it exists
   - **Features**: Key features or capabilities as bullet points
   - **Tech Stack**: Languages, frameworks, and major dependencies
   - **Project Structure**: Tree or table showing the directory layout and what each part does
   - **Getting Started**:
     - Prerequisites (runtime versions, tools needed)
     - Installation steps
     - Configuration / environment variables (if any)
   - **Usage**: How to run the project, example commands, or code snippets
   - **Scripts / Commands**: Table of available npm scripts, make targets, or CLI commands
   - **Testing**: How to run tests
   - **Contributing**: Brief contribution guidelines if applicable
   - **License**: License info if a LICENSE file exists

3. **Guidelines**:
   - Only include sections that are relevant — skip empty or inapplicable ones
   - Use clear markdown formatting with headers, code blocks, and tables
   - Keep descriptions accurate to what the code actually does — do not fabricate features
   - If the repo is small or new, keep the README proportionally brief but still well-structured
   - Preserve any existing content that is still accurate, and update or replace outdated parts
