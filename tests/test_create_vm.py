import pytest
from unittest.mock import patch, MagicMock
from create_vm import create_vm


@patch("create_vm.subprocess.run")
def test_create_vm_success(mock_run):
    """Test successful VM creation."""
    mock_run.return_value = MagicMock(stdout="Instance created successfully")
    
    create_vm("test-vm-1")
    
    mock_run.assert_called_once()
    call_args = mock_run.call_args[0][0]
    assert "gcloud" in call_args
    assert "compute" in call_args
    assert "instances" in call_args
    assert "create" in call_args
    assert "test-vm-1" in call_args
    assert "--zone=us-central1-a" in call_args


@patch("create_vm.subprocess.run")
def test_create_vm_failure(mock_run):
    """Test VM creation failure handling."""
    from subprocess import CalledProcessError
    
    error = CalledProcessError(1, "gcloud", stderr="Error message")
    mock_run.side_effect = error
    
    with pytest.raises(SystemExit) as exc_info:
        create_vm("test-vm-1")
    
    assert exc_info.value.code == 1


@patch("create_vm.subprocess.run")
def test_create_vm_with_special_name(mock_run):
    """Test VM creation with special characters in name."""
    mock_run.return_value = MagicMock(stdout="Success")
    
    create_vm("test-vm-prod-001")
    
    mock_run.assert_called_once()
    call_args = mock_run.call_args[0][0]
    assert "test-vm-prod-001" in call_args
