import pytest
from unittest.mock import patch, MagicMock
from delete_vm import delete_vm


@patch("delete_vm.subprocess.run")
def test_delete_vm_success(mock_run):
    """Test successful VM deletion."""
    mock_run.return_value = MagicMock(stdout="Instance deleted successfully")
    
    delete_vm("test-vm-1")
    
    mock_run.assert_called_once()
    call_args = mock_run.call_args[0][0]
    assert "gcloud" in call_args
    assert "compute" in call_args
    assert "instances" in call_args
    assert "delete" in call_args
    assert "test-vm-1" in call_args
    assert "--zone=us-central1-a" in call_args
    assert "--quiet" in call_args


@patch("delete_vm.subprocess.run")
def test_delete_vm_failure(mock_run):
    """Test VM deletion failure handling."""
    from subprocess import CalledProcessError
    
    error = CalledProcessError(1, "gcloud", stderr="Error message")
    mock_run.side_effect = error
    
    with pytest.raises(SystemExit) as exc_info:
        delete_vm("test-vm-1")
    
    assert exc_info.value.code == 1


@patch("delete_vm.subprocess.run")
def test_delete_vm_with_quiet_flag(mock_run):
    """Test that delete operation includes --quiet flag."""
    mock_run.return_value = MagicMock(stdout="Success")
    
    delete_vm("test-vm-prod")
    
    mock_run.assert_called_once()
    call_args = mock_run.call_args[0][0]
    assert "--quiet" in call_args
