import click
from create_vm import create_vm
from delete_vm import delete_vm
from list_vms import list_vms


@click.group()
def manage_openclaw():
    """Manage OpenClaw Google Cloud VM instances."""
    pass


@manage_openclaw.command()
def list():
    """List all OpenClaw VM instances in us-central1-a."""
    list_vms()


@manage_openclaw.command()
@click.argument("name")
def create(name):
    """Create a new OpenClaw VM instance.
    
    NAME is the name for the new VM instance.
    """
    create_vm(name)


@manage_openclaw.command()
@click.argument("name")
def delete(name):
    """Delete an OpenClaw VM instance.
    
    NAME is the name of the VM instance to delete.
    """
    delete_vm(name)


if __name__ == "__main__":
    manage_openclaw()
