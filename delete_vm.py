import subprocess
import sys
import argparse

def delete_vm(vm_name):
    zone = "us-central1-a"
    
    # Define the gcloud command
    command = [
        "gcloud", "compute", "instances", "delete", vm_name,
        "--zone=" + zone,
        "--quiet"
    ]
    
    print(f"Deleting instance: {vm_name} from zone: {zone}...")
    
    try:
        # Run the command and wait for it to complete
        result = subprocess.run(command, check=True, capture_output=True, text=True)
        print("Successfully deleted the instance!")
        print(result.stdout)
    except subprocess.CalledProcessError as e:
        print(f"Error deleting instance: {e}")
        print(f"Details: {e.stderr}")
        sys.exit(1)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Delete a Google Cloud VM instance.")
    parser.add_argument("name", help="The name of the VM instance to delete")
    
    args = parser.parse_args()
    delete_vm(args.name)
