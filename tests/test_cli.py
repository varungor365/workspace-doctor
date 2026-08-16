from pathlib import Path

from workspace_doctor.cli import expected_version, find_root, inspect


def test_expected_version(tmp_path: Path):
    (tmp_path / ".python-version").write_text("3.12.1\n")
    assert expected_version(tmp_path, ".python-version") == "3.12.1"


def test_inspect_detects_project_and_env(tmp_path: Path):
    (tmp_path / "pyproject.toml").write_text("[project]\nname='demo'\n")
    (tmp_path / ".env").write_text("TOKEN=secret\n")
    checks = {item.name: item for item in inspect(tmp_path)}
    assert checks["project"].status == "pass"
    assert checks[".env"].status == "warn"


def test_find_root_falls_back_to_directory(tmp_path: Path):
    assert find_root(tmp_path) == tmp_path.resolve()
