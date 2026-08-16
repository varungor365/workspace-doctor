from __future__ import annotations

import argparse
import json
import os
import shutil
import subprocess
import sys
from dataclasses import asdict, dataclass
from pathlib import Path


@dataclass
class Check:
    name: str
    status: str
    detail: str
    hint: str = ""


def run_version(command: str, args: tuple[str, ...] = ("--version",)) -> str | None:
    if not shutil.which(command):
        return None
    try:
        result = subprocess.run([command, *args], capture_output=True, text=True, timeout=5, check=False)
    except (OSError, subprocess.TimeoutExpired):
        return None
    text = (result.stdout or result.stderr).strip().splitlines()
    return text[0][:160] if text else None


def find_root(start: Path) -> Path:
    start = start.resolve()
    if start.is_file():
        start = start.parent
    try:
        result = subprocess.run(["git", "-C", str(start), "rev-parse", "--show-toplevel"], capture_output=True, text=True, timeout=5, check=False)
        if result.returncode == 0 and result.stdout.strip():
            return Path(result.stdout.strip()).resolve()
    except (OSError, subprocess.TimeoutExpired):
        pass
    return start


def expected_version(root: Path, filename: str) -> str | None:
    path = root / filename
    if not path.is_file():
        return None
    value = path.read_text(encoding="utf-8", errors="replace").strip().splitlines()
    return value[0].strip() if value else None


def inspect(root: Path) -> list[Check]:
    checks: list[Check] = []
    git = run_version("git")
    checks.append(Check("git", "pass" if git else "warn", git or "git is not available", "Install Git or run this inside a Git-aware environment."))
    markers = {
        "pyproject.toml": "Python project metadata",
        "package.json": "Node project metadata",
        "Dockerfile": "Docker build file",
        "docker-compose.yml": "Docker Compose file",
        "compose.yml": "Docker Compose file",
        "Makefile": "Make task runner",
        "poetry.lock": "Poetry lockfile",
        "uv.lock": "uv lockfile",
        "package-lock.json": "npm lockfile",
        "pnpm-lock.yaml": "pnpm lockfile",
    }
    found = []
    for filename, label in markers.items():
        if (root / filename).exists():
            found.append(label)
    checks.append(Check("project", "pass" if found else "warn", ", ".join(dict.fromkeys(found)) if found else "no common project marker found", "Add clear project metadata if this is a source repository."))
    for command, label in (("python", "Python runtime"), ("node", "Node runtime"), ("docker", "Docker runtime")):
        version = run_version(command)
        checks.append(Check(command, "pass" if version else "info", version or f"{label} not found", "Install it only if this project needs it."))
    for filename, command, label in ((".python-version", "python", "Python version hint"), (".nvmrc", "node", "Node version hint")):
        wanted = expected_version(root, filename)
        if wanted:
            checks.append(Check(filename, "info", f"project requests {wanted}", f"Compare the active {label.lower()} with the project hint."))
    env_files = [p.name for p in root.iterdir() if p.is_file() and (p.name == ".env" or p.name.startswith(".env.")) and p.name not in {".env.example", ".env.sample"}]
    if env_files:
        checks.append(Check(".env", "warn", f"found {', '.join(env_files)}", "Do not commit or paste values; inspect with envsafe and keep secrets local."))
    else:
        checks.append(Check(".env", "pass", "no private environment file detected", ""))
    return checks


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Read-only project environment diagnostics")
    parser.add_argument("path", nargs="?", default=".")
    parser.add_argument("--json", action="store_true", dest="as_json")
    args = parser.parse_args(argv)
    root = find_root(Path(args.path))
    checks = inspect(root)
    payload = {"path": str(root), "checks": [asdict(check) for check in checks]}
    if args.as_json:
        print(json.dumps(payload, indent=2))
    else:
        print(f"workspace-doctor: {root}")
        for check in checks:
            suffix = f" — {check.hint}" if check.hint and check.status in {"warn", "info"} else ""
            print(f"{check.status.upper():5} {check.name:16} {check.detail}{suffix}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
