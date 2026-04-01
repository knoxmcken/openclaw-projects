import subprocess
import sys

def list_vms():
    zone = "us-central1-a"
    
    # Define the gcloud command
    command = [
        "gcloud", "compute", "instances", "list",
        "--zones=" + zone,
        "--format=table(name,status,INTERNAL_IP,EXTERNAL_IP)"
    ]
    
    print(f"Listing instances in zone: {zone}...\n")
    
    try:
        # Run the command and wait for it to complete
        result = subprocess.run(command, check=True, capture_output=True, text=True)
        print(result.stdout)
    except subprocess.CalledProcessError as e:
        print(f"Error listing instances: {e}")
        print(f"Details: {e.stderr}")
        sys.exit(1)

if __name__ == "__main__":
    list_vms()
