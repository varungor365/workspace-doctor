#!/usr/bin/env bash
set -euo pipefail

demo_dir="$(mktemp -d)"
trap 'rm -rf "$demo_dir"' EXIT

git -C "$demo_dir" init -q
printf '[build-system]\nrequires = []\n' > "$demo_dir/pyproject.toml"
printf 'DEMO_ONLY=not-a-secret\n' > "$demo_dir/.env.example"
workspace_doctor "$demo_dir"
printf '\nJSON output:\n'
workspace_doctor --json "$demo_dir"
