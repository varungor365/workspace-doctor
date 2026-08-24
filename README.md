# workspace-doctor: Project Setup Diagnostics

**Diagnose a project setup before you lose an hour to a broken environment.**

`workspace-doctor` is a local, read-only CLI that inspects a repository, detects common Python/Node/Docker project markers, checks available tool versions, and prints actionable setup hints. It never installs packages, edits files, or uploads source code.

## Quick start

```bash
pipx install workspace-doctor
cd path/to/project
workspace_doctor
workspace_doctor --json > workspace-health.json
```

Example output:

```text
PASS  git          git version 2.45.2
PASS  project      pyproject.toml detected
WARN  node         not installed; skip Node checks if this is a Python-only project
WARN  .env         found; inspect it with envsafe before sharing the repository
```

## What it checks

The doctor locates the Git root, detects `pyproject.toml`, `package.json`, Docker files, lockfiles, version-manager files, and environment files, then reports whether common local tools are available. Output is human-readable by default and stable JSON with `--json` for CI or issue templates.

All checks are local and read-only. A warning is a prompt for investigation, not proof that a project is broken.

## Why star this repository

Star this project if you maintain Python, Node, or Docker repositories, help other developers troubleshoot setup issues, or want a small diagnostic CLI to extend with project-specific checks.

## Development

```bash
git clone https://github.com/varungor365/workspace-doctor
cd workspace-doctor
python -m pip install -e ".[dev]"
pytest -q
```

## License

MIT.
