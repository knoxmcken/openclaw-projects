import sys
from pathlib import Path

try:
    import tomllib
except ImportError:
    import tomli as tomllib

_CONFIG_FILE = Path(__file__).parent / "openclaw-config.toml"

_DEFAULTS = {
    "zone": "us-central1-a",
    "machine_type": "e2-medium",
    "disk_size": "10",
    "service_account": "828463118397-compute@developer.gserviceaccount.com",
    "project_id": "gcp-labs-01-350902",
}


def gcloud_exe() -> str:
    return "gcloud.cmd" if sys.platform == "win32" else "gcloud"


def load_config() -> dict:
    if not _CONFIG_FILE.exists():
        return _DEFAULTS.copy()
    with open(_CONFIG_FILE, "rb") as f:
        data = tomllib.load(f)
    return {**_DEFAULTS, **data.get("vm", {})}
