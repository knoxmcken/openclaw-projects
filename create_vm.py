import subprocess
import sys
import argparse

def create_vm(new_name):
    zone = "us-central1-a"
    machine_type = "e2-medium"
    disk_size = "10"
    service_account = "828463118397-compute@developer.gserviceaccount.com"
    
    # Define scopes
    scopes = [
        "https://www.googleapis.com/auth/devstorage.read_only",
        "https://www.googleapis.com/auth/logging.write",
        "https://www.googleapis.com/auth/monitoring.write",
        "https://www.googleapis.com/auth/service.management.readonly",
        "https://www.googleapis.com/auth/servicecontrol",
        "https://www.googleapis.com/auth/trace.append"
    ]
    
    # Define the gcloud command
    command = [
        "gcloud", "compute", "instances", "create", new_name,
        "--zone=" + zone,
        "--machine-type=" + machine_type,
        "--network-interface=network-tier=PREMIUM,stack-type=IPV4_ONLY,subnet=default",
        "--maintenance-policy=MIGRATE",
        "--provisioning-model=STANDARD",
        "--service-account=" + service_account,
        "--scopes=" + ",".join(scopes),
        f"--create-disk=auto-delete=yes,boot=yes,device-name={new_name},image=projects/debian-cloud/global/images/family/debian-12,mode=read-write,size={disk_size},type=projects/gcp-labs-01-350902/zones/us-central1-a/diskTypes/pd-balanced",
        "--no-shielded-secure-boot",
        "--shielded-vtpm",
        "--shielded-integrity-monitoring",
        "--labels=goog-ops-agent-policy=v2-template-1-5-0",
        "--metadata=enable-osconfig=TRUE",
        "--reservation-affinity=any"
    ]
    
    print(f"Creating instance: {new_name} in zone: {zone}...")
    
    try:
        # Run the command and wait for it to complete
        result = subprocess.run(command, check=True, capture_output=True, text=True)
        print("Successfully created the instance!")
        print(result.stdout)
    except subprocess.CalledProcessError as e:
        print(f"Error creating instance: {e}")
        print(f"Details: {e.stderr}")
        sys.exit(1)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Create a Google Cloud VM based on open-claw-1 properties.")
    parser.add_item = parser.add_argument("name", help="The name for the new VM instance")
    
    args = parser.parse_args()
    create_vm(args.name)
