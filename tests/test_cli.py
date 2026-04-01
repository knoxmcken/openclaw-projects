import pytest
from click.testing import CliRunner
from unittest.mock import patch, MagicMock
from cli import manage_openclaw


@pytest.fixture
def runner():
    """Fixture for Click CLI runner."""
    return CliRunner()


def test_cli_create_command(runner):
    """Test CLI create command."""
    with patch("cli.create_vm") as mock_create:
        result = runner.invoke(manage_openclaw, ["create", "test-vm"])
        
        assert result.exit_code == 0
        mock_create.assert_called_once_with("test-vm")


def test_cli_delete_command(runner):
    """Test CLI delete command."""
    with patch("cli.delete_vm") as mock_delete:
        result = runner.invoke(manage_openclaw, ["delete", "test-vm"])
        
        assert result.exit_code == 0
        mock_delete.assert_called_once_with("test-vm")


def test_cli_list_command(runner):
    """Test CLI list command."""
    with patch("cli.list_vms") as mock_list:
        result = runner.invoke(manage_openclaw, ["list"])
        
        assert result.exit_code == 0
        mock_list.assert_called_once()


def test_cli_help(runner):
    """Test CLI help output."""
    result = runner.invoke(manage_openclaw, ["--help"])
    
    assert result.exit_code == 0
    assert "Manage OpenClaw" in result.output
    assert "list" in result.output
    assert "create" in result.output
    assert "delete" in result.output


def test_cli_create_requires_name(runner):
    """Test that create command requires a name argument."""
    result = runner.invoke(manage_openclaw, ["create"])
    
    assert result.exit_code != 0
    assert "Missing argument" in result.output or "missing" in result.output.lower()


def test_cli_delete_requires_name(runner):
    """Test that delete command requires a name argument."""
    result = runner.invoke(manage_openclaw, ["delete"])
    
    assert result.exit_code != 0
    assert "Missing argument" in result.output or "missing" in result.output.lower()
