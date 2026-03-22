"""Hook: Generate/update requirements.txt when the update-readme skill runs.

Reads hook event data from stdin, checks if the skill is 'update-readme',
then scans all Python files for third-party imports using pipreqs via uv.
"""

import sys
import json
import subprocess
from pathlib import Path


def main():
    # Read hook event data from stdin
    try:
        data = json.load(sys.stdin)
    except Exception:
        sys.exit(0)

    # Only run for the update-readme skill
    tool_input = data.get("tool_input", {})
    skill = tool_input.get("skill", "")
    if skill != "update-readme":
        sys.exit(0)

    # Check if there are any Python files to scan
    py_files = list(Path(".").rglob("*.py"))
    # Exclude hook scripts themselves
    py_files = [f for f in py_files if ".claude/hooks" not in str(f).replace("\\", "/")]

    if not py_files:
        print("No Python files found — skipping requirements.txt generation")
        sys.exit(0)

    # Try pipreqs via uv (auto-installs if needed)
    try:
        result = subprocess.run(
            ["python", "-m", "uv", "tool", "run", "pipreqs", ".", "--force",
             "--ignore", ".claude"],
            capture_output=True,
            text=True,
        )
        if result.returncode == 0:
            print("requirements.txt updated successfully")
            sys.exit(0)
    except FileNotFoundError:
        pass

    # Fallback: try pipreqs directly
    try:
        result = subprocess.run(
            ["pipreqs", ".", "--force", "--ignore", ".claude"],
            capture_output=True,
            text=True,
        )
        if result.returncode == 0:
            print("requirements.txt updated successfully")
            sys.exit(0)
    except FileNotFoundError:
        pass

    # Final fallback: manual import scan
    print("pipreqs not available — falling back to manual import scan")
    scan_and_generate(py_files)


def scan_and_generate(py_files):
    """Scan Python files for imports and write requirements.txt."""
    import importlib.util

    imports = set()
    for f in py_files:
        try:
            content = f.read_text(encoding="utf-8")
            for line in content.splitlines():
                stripped = line.strip()
                if stripped.startswith("import "):
                    # Handle: import foo, import foo.bar, import foo as bar
                    parts = stripped[7:].split(",")
                    for part in parts:
                        mod = part.strip().split(".")[0].split(" ")[0]
                        if mod:
                            imports.add(mod)
                elif stripped.startswith("from ") and " import " in stripped:
                    # Handle: from foo import bar, from foo.bar import baz
                    mod = stripped[5:].split(" import ")[0].split(".")[0].strip()
                    if mod and not mod.startswith("."):
                        imports.add(mod)
        except Exception:
            continue

    # Filter out standard library modules
    stdlib = set()
    for mod in imports:
        try:
            spec = importlib.util.find_spec(mod)
            if spec is not None:
                origin = getattr(spec, "origin", "") or ""
                if "site-packages" not in origin and "dist-packages" not in origin:
                    stdlib.add(mod)
        except (ModuleNotFoundError, ValueError):
            # Module not installed locally — likely third-party, keep it
            pass

    third_party = sorted(imports - stdlib)
    if third_party:
        Path("requirements.txt").write_text("\n".join(third_party) + "\n")
        print(f"requirements.txt updated with {len(third_party)} packages")
    else:
        print("No third-party packages detected — skipping requirements.txt")


if __name__ == "__main__":
    main()
