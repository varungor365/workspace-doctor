# workspace-doctor: Python, Node.js, and Docker Setup Diagnostics

[![CI](https://github.com/varungor365/workspace-doctor/actions/workflows/ci.yml/badge.svg)](https://github.com/varungor365/workspace-doctor/actions/workflows/ci.yml)

**Diagnose a project setup before you lose an hour to a broken environment.**

`workspace-doctor` is a local, read-only CLI that inspects a repository, detects common Python, Node.js, and Docker project markers, checks available tool versions, and prints actionable setup hints. It never installs packages, edits files, or uploads source code.

## Why this exists

Setup failures often come from small mismatches: a missing runtime, an unexpected lockfile, a version-manager file, or an environment file that should not be shared. This tool provides a fast first pass before deeper debugging or opening a support issue.

| Use case | Output |
|---|---|
| New project onboarding | A quick health check for local runtimes and project markers. |
| Support requests | Stable JSON that can be attached to an issue without uploading source files. |
| CI preflight | A local-only diagnostic step before expensive builds. |
| Mixed-language repositories | One command that recognizes Python, Node.js, and Docker signals. |

## Three-minute quick start

For a disposable demo that creates a temporary Git repository and runs read-only checks, use [examples/health-check.sh](examples/health-check.sh).

```bash
python -m venv .venv
. .venv/bin/activate
python -m pip install workspace-doctor
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

## Safe defaults and limitations

`workspace-doctor` does not install dependencies, execute project build scripts, inspect source-code correctness, validate credentials, or access the network. Tool-version checks describe what is available on the current machine; they do not prove that a project is compatible with every version. Review warnings in the context of the repository's own documentation and lockfiles.

## Why star this repository?

Star this project if you maintain Python, Node.js, or Docker repositories, help other developers troubleshoot setup issues, or want a small diagnostic CLI to extend with project-specific checks.

## Development

```bash
git clone https://github.com/varungor365/workspace-doctor
cd workspace-doctor
python -m pip install -e '.[dev]'
pytest -q
```

## License

MIT. See [LICENSE](LICENSE).
