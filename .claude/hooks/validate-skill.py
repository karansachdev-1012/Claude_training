"""Hook: Validate skill files after they are written or edited.

Runs as a PostToolUse hook on Write|Edit. Reads the tool input from stdin,
checks if the modified file is a SKILL.md, and runs structural validation.
If issues are found, prints warnings and suggests running the
skills-troubleshooter agent for a full diagnosis.
"""

import sys
import json
import re
from pathlib import Path


def main():
    # Read hook event data from stdin
    try:
        data = json.load(sys.stdin)
    except Exception:
        sys.exit(0)

    # Extract the file path from the tool input
    tool_input = data.get("tool_input", {})
    file_path = tool_input.get("file_path", "")

    if not file_path:
        sys.exit(0)

    # Normalize path separators
    normalized = file_path.replace("\\", "/")

    # Only run for SKILL.md files inside .claude/skills/
    if ".claude/skills/" not in normalized or not normalized.endswith("/SKILL.md"):
        sys.exit(0)

    # Run validation
    path = Path(file_path)
    if not path.exists():
        sys.exit(0)

    issues = []
    warnings = []

    try:
        content = path.read_text(encoding="utf-8")
    except Exception as e:
        print(f"Could not read {file_path}: {e}")
        sys.exit(0)

    lines = content.splitlines()

    # Check 1: Directory structure
    parts = normalized.split(".claude/skills/")
    if len(parts) == 2:
        remainder = parts[1]  # e.g., "commit/SKILL.md"
        segments = remainder.strip("/").split("/")
        if len(segments) < 2:
            issues.append("SKILL.md must be inside a named subdirectory (e.g., .claude/skills/my-skill/SKILL.md)")

    # Check 2: Frontmatter exists
    has_frontmatter = False
    name_field = None
    description_field = None

    if content.startswith("---"):
        end_idx = content.find("---", 3)
        if end_idx != -1:
            has_frontmatter = True
            frontmatter = content[3:end_idx].strip()

            # Check name field
            name_match = re.search(r"^name:\s*(.+)$", frontmatter, re.MULTILINE)
            if name_match:
                name_field = name_match.group(1).strip().strip("\"'")
            else:
                issues.append("Missing 'name' field in frontmatter")

            # Check description field
            desc_match = re.search(r"^description:\s*(.+)$", frontmatter, re.MULTILINE)
            if desc_match:
                description_field = desc_match.group(1).strip().strip("\"'")
            else:
                issues.append("Missing 'description' field in frontmatter")

    if not has_frontmatter:
        issues.append("Missing YAML frontmatter (must start with --- and end with ---)")

    # Check 3: Description quality
    if description_field:
        if len(description_field) > 1024:
            issues.append(f"Description is {len(description_field)} chars (max 1024)")

        # Check for trigger phrases
        trigger_keywords = ["use when", "when the user", "when you", "ask", "say"]
        has_trigger_hint = any(kw in description_field.lower() for kw in trigger_keywords)
        if not has_trigger_hint:
            warnings.append("Description may lack trigger phrases — add phrases like 'Use when the user asks...' for better matching")

    # Check 4: Line count
    line_count = len(lines)
    if line_count > 500:
        # Check for progressive disclosure
        skill_dir = path.parent
        has_refs = (skill_dir / "references").is_dir()
        has_assets = (skill_dir / "assets").is_dir()
        if not has_refs and not has_assets:
            issues.append(f"File is {line_count} lines (max 500) — consider using progressive disclosure with references/ or assets/ directories")
        else:
            warnings.append(f"File is {line_count} lines but uses progressive disclosure — acceptable")

    # Check 5: Path separators
    if "\\\\" in content or re.search(r"(?<!\\)\\(?![\\n\"'])", content):
        warnings.append("Found backslash paths — use forward slashes (/) for cross-platform compatibility")

    # Print results
    skill_name = name_field or "unknown"

    if issues:
        print(f"--- Skill validation FAILED for '{skill_name}' ---")
        for issue in issues:
            print(f"  FAIL: {issue}")
        for warning in warnings:
            print(f"  WARN: {warning}")
        print("  Tip: Run the skills-troubleshooter agent for a full diagnosis")
    elif warnings:
        print(f"--- Skill validation PASSED with warnings for '{skill_name}' ---")
        for warning in warnings:
            print(f"  WARN: {warning}")
    else:
        print(f"--- Skill validation PASSED for '{skill_name}' ---")


if __name__ == "__main__":
    main()
