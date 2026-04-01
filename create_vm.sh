#!/bin/bash

# Script to create a new Google Cloud VM based on the properties of open-claw-1
# Usage: ./create_vm.sh <new-instance-name>

if [ -z "$1" ]; then
    echo "Error: No instance name provided."
    echo "Usage: $0 <new-instance-name>"
    exit 1
fi

NEW_NAME=$1
ZONE="us-central1-a"
MACHINE_TYPE="e2-medium"
IMAGE_PROJECT="debian-cloud"
IMAGE_FAMILY="debian-12"
DISK_SIZE="10"

echo "Creating instance: $NEW_NAME in zone: $ZONE..."

gcloud compute instances create "$NEW_NAME" \
    --zone="$ZONE" \
    --machine-type="$MACHINE_TYPE" \
    --network-interface=network-tier=PREMIUM,stack-type=IPV4_ONLY,subnet=default \
    --maintenance-policy=MIGRATE \
    --provisioning-model=STANDARD \
    --service-account=828463118397-compute@developer.gserviceaccount.com \
    --scopes=https://www.googleapis.com/auth/devstorage.read_only,https://www.googleapis.com/auth/logging.write,https://www.googleapis.com/auth/monitoring.write,https://www.googleapis.com/auth/service.management.readonly,https://www.googleapis.com/auth/servicecontrol,https://www.googleapis.com/auth/trace.append \
    --create-disk=auto-delete=yes,boot=yes,device-name="$NEW_NAME",image=projects/debian-cloud/global/images/family/debian-12,mode=read-write,size="$DISK_SIZE",type=projects/gcp-labs-01-350902/zones/us-central1-a/diskTypes/pd-balanced \
    --no-shielded-secure-boot \
    --shielded-vtpm \
    --shielded-integrity-monitoring \
    --labels=goog-ops-agent-policy=v2-template-1-5-0 \
    --metadata=enable-osconfig=TRUE \
    --reservation-affinity=any
