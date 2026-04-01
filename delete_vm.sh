#!/bin/bash

# Script to delete a Google Cloud VM instance
# Usage: ./delete_vm.sh <instance-name>

if [ -z "$1" ]; then
    echo "Error: No instance name provided."
    echo "Usage: $0 <instance-name>"
    exit 1
fi

VM_NAME=$1
ZONE="us-central1-a"

echo "Deleting instance: $VM_NAME from zone: $ZONE..."

gcloud compute instances delete "$VM_NAME" \
    --zone="$ZONE" \
    --quiet
