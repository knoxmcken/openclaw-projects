# Copilot Instructions for openclaw-vm-scripts

## Project Overview

openclaw-vm-scripts is a Google Cloud Platform (GCP) VM management utility suite. It provides Python and Bash scripts for creating, deleting, and listing Debian 12 VM instances in GCP's `us-central1-a` zone. All instances are configured with e2-medium machine type and standard GCP scopes for logging, monitoring, and service management.

## Architecture & Design

**Key Design Patterns:**
- **Dual Implementation**: Each management operation (create, delete, list) has both Python and Bash implementations for flexibility. Bash scripts are portable shell wrappers; Python scripts provide structured CLI with argument parsing.
- **Consistent Configuration**: All scripts hardcode the same zone (`us-central1-a`), machine type (`e2-medium`), and service account to maintain infrastructure consistency.
- **Bash Validation**: Bash scripts include input validation (checking for required arguments); Python scripts use argparse for structured argument handling.

**Python Script Structure:**
1. Main function contains all logic
2. Uses `subprocess.run()` with `check=True` for error handling
3. Captures stdout/stderr for user feedback
4. Exits with status code 1 on error

**Bash Script Structure:**
1. Validates input arguments at start
2. Uses variables for configuration (ZONE, MACHINE_TYPE, etc.)
3. Single multi-line `gcloud` command with backslash line continuations
4. Uses `--quiet` flag to suppress confirmation prompts

## Virtual Environment

**IMPORTANT:** Always use the `.venv-openclaw` virtual environment for all Python operations.

**Setup (one-time):**
If `.venv-openclaw` doesn't exist, create it:
```bash
python -m venv .venv-openclaw
```

**Activation:**
- Windows: `.venv-openclaw\Scripts\activate`
- Unix/macOS: `source .venv-openclaw/bin/activate`

After activation, all `python` and `pip` commands use the isolated environment.

## Build, Test & Lint

**No build step required.** Scripts can be run directly.

**Installation for CLI usage (within venv):**
```bash
pip install -e .
```

This installs the package in editable mode and registers CLI entry points (manage-openclaw with subcommands list, create, delete).

**Running scripts directly:**
- Python: `python create_vm.py <instance-name>`
- Bash: `./create_vm.sh <instance-name>`
- CLI: `manage-openclaw create <instance-name>`

**Development dependencies:**
```bash
pip install -e ".[dev]"
```

Installs pytest, black (code formatter), and flake8 (linter) as configured in pyproject.toml.

**Formatting:**
```bash
black .
```

Enforces 88-character line length (configured in pyproject.toml).

**Linting:**
```bash
flake8 .
```

Standard flake8 checks (no custom configuration).

## Key Conventions

1. **GCP Zone Hardcoding**: All scripts hardcode `us-central1-a`. Do not parameterize this without updating all four scripts to maintain consistency.

2. **Service Account**: Service account email is hardcoded in all scripts. This is intentional for infrastructure consistency.

3. **Error Handling Pattern**: 
   - Python: `subprocess.CalledProcessError` caught with stderr printed
   - Bash: No explicit error handling; relies on `gcloud`'s exit codes
   - Both print the command being executed before running it

4. **No External Dependencies**: Python scripts use only stdlib (subprocess, sys, argparse). Keep it this way to ensure zero installation friction for GCP-authenticated users.

5. **Quiet Flag**: Both delete operations use `--quiet` to skip confirmation prompts, enabling automation. Create operations do not suppress confirmations intentionally.

6. **Script File Permissions**: Bash scripts should have execute permission (`chmod +x *.sh`) but this is not enforced in the repo.

## Common Tasks

**Adding a new GCP parameter** (e.g., adding labels or metadata):
- Update the hardcoded value in both the Python function and the Bash variables
- Update all four scripts (create_vm.py, create_vm.sh, and corresponding list/delete if applicable)
- Test with actual gcloud CLI to verify parameter syntax

**Extending to other zones:**
- Instead of hardcoding, add a command-line argument to accept zone parameter
- Update all four scripts consistently
- Ensure zone validation matches gcloud's allowed zones

**Adding logging or monitoring:**
- Keep Python scripts minimal; add logging to the main functions if needed
- Bash scripts should continue to rely on standard output for visibility
- Consider adding `--format=json` option to list_vms for machine-readable output

## Files Overview

- `create_vm.py` / `create_vm.sh`: Create new VM instances
- `delete_vm.py` / `delete_vm.sh`: Delete VM instances (uses `--quiet`)
- `list_vms.py` / `list_vms.sh`: List instances with formatted output
- `pyproject.toml`: Package metadata, entry points, and tool configuration
