import pytest
from unittest.mock import patch, MagicMock
from list_vms import list_vms


@patch("list_vms.subprocess.run")
def test_list_vms_success(mock_run):
    """Test successful VM listing."""
    mock_output = "NAME\ntest-vm-1\ntest-vm-2\n"
    mock_run.return_value = MagicMock(stdout=mock_output)
    
    list_vms()
    
    mock_run.assert_called_once()
    call_args = mock_run.call_args[0][0]
    assert "gcloud" in call_args
    assert "compute" in call_args
    assert "instances" in call_args
    assert "list" in call_args
    assert "--zones=us-central1-a" in call_args
    assert "--format=table(name,status,INTERNAL_IP,EXTERNAL_IP)" in call_args


@patch("list_vms.subprocess.run")
def test_list_vms_failure(mock_run):
    """Test VM listing failure handling."""
    from subprocess import CalledProcessError
    
    error = CalledProcessError(1, "gcloud", stderr="Error message")
    mock_run.side_effect = error
    
    with pytest.raises(SystemExit) as exc_info:
        list_vms()
    
    assert exc_info.value.code == 1


@patch("list_vms.subprocess.run")
def test_list_vms_format(mock_run):
    """Test that list operation uses correct format."""
    mock_run.return_value = MagicMock(stdout="")
    
    list_vms()
    
    mock_run.assert_called_once()
    call_args = mock_run.call_args[0][0]
    assert "--format=table(name,status,INTERNAL_IP,EXTERNAL_IP)" in call_args
