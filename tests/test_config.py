import pytest
from pathlib import Path
from unittest.mock import patch, mock_open
from config import load_config, _DEFAULTS


def test_load_config_file_missing(tmp_path):
    with patch("config._CONFIG_FILE", tmp_path / "nonexistent.toml"):
        result = load_config()
    assert result == _DEFAULTS
    assert result is not _DEFAULTS  # returns a copy


def test_load_config_all_keys(tmp_path):
    toml_content = b"""
[vm]
zone = "europe-west1-b"
machine_type = "e2-small"
disk_size = "20"
service_account = "custom@project.iam.gserviceaccount.com"
project_id = "my-project"
"""
    config_file = tmp_path / "openclaw-config.toml"
    config_file.write_bytes(toml_content)

    with patch("config._CONFIG_FILE", config_file):
        result = load_config()

    assert result["zone"] == "europe-west1-b"
    assert result["machine_type"] == "e2-small"
    assert result["disk_size"] == "20"
    assert result["service_account"] == "custom@project.iam.gserviceaccount.com"
    assert result["project_id"] == "my-project"


def test_load_config_partial_overrides_defaults(tmp_path):
    toml_content = b"""
[vm]
zone = "us-east1-b"
"""
    config_file = tmp_path / "openclaw-config.toml"
    config_file.write_bytes(toml_content)

    with patch("config._CONFIG_FILE", config_file):
        result = load_config()

    assert result["zone"] == "us-east1-b"
    assert result["machine_type"] == _DEFAULTS["machine_type"]
    assert result["disk_size"] == _DEFAULTS["disk_size"]
    assert result["service_account"] == _DEFAULTS["service_account"]
    assert result["project_id"] == _DEFAULTS["project_id"]
