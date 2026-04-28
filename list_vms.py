import subprocess
import sys
from config import load_config, gcloud_exe

def list_vms():
    cfg = load_config()
    zone = cfg["zone"]
    
    # Define the gcloud command
    command = [
        gcloud_exe(), "compute", "instances", "list",
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
