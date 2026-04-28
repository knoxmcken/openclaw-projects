# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Virtual Environment

Always use the `.venv-openclaw` virtual environment. Activate with `.venv-openclaw\Scripts\activate` (Windows) or `source .venv-openclaw/bin/activate` (Unix).

## Commands

```bash
# Install package + CLI entry points
pip install -e .

# Install with dev dependencies (pytest, black, flake8)
pip install -e ".[dev]"

# Run all tests
pytest

# Run a single test file
pytest tests/test_cli.py

# Run a single test
pytest tests/test_cli.py::test_cli_create_command

# Format
black .

# Lint
flake8 .
```

## CLI Entry Points

After `pip install -e .`, two aliases are registered pointing to the same Click group:
- `manage-openclaw`
- `oc`

Subcommands: `list`, `create <name>`, `delete <name>`

## Architecture

**Dual implementation**: each operation (create, delete, list) has a Python module (`create_vm.py`, etc.) and a Bash script (`create_vm.sh`, etc.). The Python modules export a single function (e.g., `create_vm(name)`) that is imported by `cli.py`. The CLI layer (`cli.py`) is a thin Click wrapper over those functions — no logic lives there.

**Configuration is fully hardcoded** across all scripts: zone (`us-central1-a`), machine type (`e2-medium`), disk size (10 GB), service account, and GCP project ID (`gcp-labs-01-350902`). When changing any of these, update both the Python module and the corresponding Bash script to keep them consistent.

**Python scripts** use `subprocess.run(..., check=True, capture_output=True, text=True)`, catch `CalledProcessError`, print `e.stderr`, and exit with code 1. Bash scripts rely on gcloud's own exit codes with no explicit error trapping.

**Tests** mock the underlying functions (not subprocess) using `unittest.mock.patch`. CLI tests use `click.testing.CliRunner`.

## Key Conventions

- Python scripts use only stdlib + click (no other third-party deps). Keep it that way.
- Delete operations pass `--quiet` to gcloud to skip confirmation prompts; create does not.
- `black` line length is 88 (configured in `pyproject.toml`).
- `create_vm.py` has a bug on line 54: `parser.add_item = parser.add_argument(...)` — this is a no-op assignment. The positional arg is never parsed when run directly as a script. The `create_vm(name)` function itself works correctly when called from the CLI.
